from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, User, Group, Competence, UserAnswer, UserResult


def home(request):
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

    return render(request, 'home.html', {'groups': groups, "message": message})


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
                user_results = UserResult.objects.filter(competence_name=competence, user=user)

                for user_result in user_results:
                    user_result.competence_count = 2
                    user_result.save()

        return redirect(f'/results/{user_id}/')

    return render(request, 'selected_questions.html',
                  {'session_selected_questions': selected_questions})




def results(request, user_id):
    user = User.objects.get(id=user_id)
    user_answers = UserAnswer.objects.get(user=user)

    user_results = UserResult.objects.filter(user=user).order_by('-competence_count')[:5]

    return render(request, 'results.html', {

        'answers': user_answers,
        'user_results': user_results
    })


def mini_admin(request):
    # Получаем все ответы пользователей
    user_answers = UserAnswer.objects.all()

    # Получаем все группы
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


def user_detail(request, user_id):
    user = User.objects.get(id=user_id)

    user_results = UserResult.objects.filter(user=user).order_by('-competence_count')
    return render(request, 'user_detail.html', {'user': user, 'user_results': user_results})
