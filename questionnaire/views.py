from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .forms import GroupForm, CompetenceForm, QuestionForm
from .models import Question, User, Group, Competence, UserAnswer, UserResult, Block
from django.contrib.auth import authenticate, login as auth_login, logout


def home(request):
    block = Block.objects.get(name='Начальный экран')
    groups = Group.objects.all()
    message = ''

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        if len(full_name.split()) == 2:
            chosen_groups_id = request.POST.get('chosen_group')
            chosen_group = Group.objects.get(id=chosen_groups_id)

            user = User.objects.create(full_name=full_name, chosen_group=chosen_group)
            user.save()

            chosen_group.users.add(user)

            user_answer = UserAnswer.objects.create(user=user, group=chosen_group)
            user_answer.save()

            return redirect(f'questions/{user.id}/')
        else:
            message = 'Введите пожалуйста Отдельно имя и фамилию. Пример: Иванов Иван'

    return render(request, 'home.html', {'groups': groups, "message": message, 'block': block})


def questions(request, user_id):
    if request.method == 'POST':
        selected_questions = {}

        questions = Question.objects.all()
        for question in questions:
            answer_text = request.POST.get(f'question_{question.id}', None)
            if answer_text == 'on':
                user = User.objects.get(id=user_id)
                competence = Competence.objects.filter(questions=question).first()
                if competence:
                    UserResult.objects.create(competence_name=competence, user=user, competence_count=1)
                    selected_questions[question.id] = competence.id

        request.session['session_selected_questions'] = selected_questions

        return redirect(f'/selected_questions/{user_id}/')

    else:
        questions = Question.objects.all()
        return render(request, 'questions.html', {'questions': questions})


def selected_questions(request, user_id):
    session_selected_questions = request.session.get('session_selected_questions', {})
    ssq = session_selected_questions.keys()
    selected_questions = []
    user = User.objects.get(id=user_id)

    for id in ssq:
        question = Question.objects.get(id=id)
        selected_questions.append(question)

    if request.method == 'POST':
        for question in selected_questions:
            answer = request.POST.get('question_' + str(question.id))
            if answer is not None:
                competence = Competence.objects.get(questions=question)
                try:
                    # Обновляем или создаем запись в UserResult
                    competence_sum = UserResult.objects.filter(user=user, competence_name=competence).aggregate(
                        Sum('competence_count')).get('competence_count__sum')
                    if competence_sum is None:
                        UserResult.objects.create(user=user, competence_name=competence, competence_count=2)
                    else:
                        UserResult.objects.update_or_create(
                            user=user,
                            competence_name=competence,
                            defaults={'competence_count': competence_sum + 2}
                        )
                except MultipleObjectsReturned:
                    UserResult.objects.filter(user=user, competence_name=competence).delete()
                    UserResult.objects.create(user=user, competence_name=competence, competence_count=2)

        return redirect(f'/results/{user_id}/')

    return render(request, 'selected_questions.html',
                  {'session_selected_questions': selected_questions})


def results(request, user_id):
    user = User.objects.get(id=user_id)
    user_answers = UserAnswer.objects.get(user=user)

    group_count = user.chosen_group.num_competences_displayed

    user_results = UserResult.objects.filter(user=user).order_by('-competence_count')[:group_count]

    return render(request, 'results.html', {

        'answers': user_answers,
        'user_results': user_results
    })

@login_required
def mini_admin(request):
    date = request.GET.get('date', '')
    group_id = request.GET.get('group', -1)
    full_name = request.GET.get('fullName', '')
    user_answers = UserAnswer.objects.all()
    groups = Group.objects.all()

    if request.method == 'POST':
        if 'group_filter' in request.POST:
            group_id = request.POST.get('group_filter')
            if group_id != '-1':
                user_answers = user_answers.filter(group_id=group_id)

        full_name = request.POST.get('full_name')
        if full_name:
            user_answers = user_answers.filter(user__full_name__icontains=full_name)

    date = request.POST.get('date')
    if date:
        parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
        user_answers = user_answers.filter(date__date=parsed_date)

    context = {
        'user_answers': user_answers,
        'groups': groups,
        'date': date
    }

    return render(request, 'mini_admin.html', context)

@login_required
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)

    user_results = UserResult.objects.filter(user=user).order_by('-competence_count')
    return render(request, 'user_detail.html', {'user': user, 'user_results': user_results})

@login_required
def group_detail(request, group_id):
    result = {}
    group = Group.objects.get(id=group_id)
    user_results = UserResult.objects.filter(user__group=group).order_by('-competence_count')

    for user_result in user_results:
        result[user_result.competence_name] = 0

    for user_result in user_results:
        result[user_result.competence_name] = result[user_result.competence_name] + user_result.competence_count

    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return render(request, 'group_detail.html', {'group': group, 'user_results': result})

@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'groups/group_list.html', {'groups': groups})

@login_required
def group_create(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    return render(request, 'groups/group_create.html', {'form': form})

@login_required
def group_update(request, pk):
    group = Group.objects.get(pk=pk)
    form = GroupForm(instance=group)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    return render(request, 'groups/group_update.html', {'form': form, 'group': group})

@login_required
def group_delete(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')
    return render(request, 'groups/group_delete.html', {'group': group})

@login_required
def competence_list(request):
    competences = Competence.objects.all()
    return render(request, 'competences/competence_list.html', {'competences': competences})

@login_required
def competence_create(request):
    form = CompetenceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('competence_list')
    return render(request, 'competences/competence_form.html', {'form': form})

@login_required
def competence_update(request, pk):
    competence = get_object_or_404(Competence, pk=pk)
    form = CompetenceForm(request.POST or None, instance=competence)
    if form.is_valid():
        form.save()
        return redirect('competence_list')
    return render(request, 'competences/competence_form.html', {'form': form})

@login_required
def competence_delete(request, pk):
    competence = get_object_or_404(Competence, pk=pk)
    if request.method == 'POST':
        competence.delete()
        return redirect('competence_list')
    return render(request, 'competences/competence_confirm_delete.html', {'competence': competence})

@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})

@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'questions/question_create.html', {'form': form})

@login_required
def question_update(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'questions/question_update.html', {'form': form})

@login_required
def question_delete(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('question_list')
    return render(request, 'questions/question_delete.html', {'question': question})


def login(request):
    message = 'Добро пожаловать! Введите ваши данные.'
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            return redirect('mini_admin')

        else:
            message = "Нет такого пользователя, просмотрите правильность написания имени и пароля"

    return render(request, 'login.html', {'message': message})
