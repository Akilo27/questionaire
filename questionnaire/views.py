from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Question, User, Group, Competence, UserAnswer


def home(request):
    groups = Group.objects.all()
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

    return render(request, 'home.html', {'groups': groups})


def questions(request, user_id):
    if request.method == 'POST':
        selected_questions = {}

        questions = Question.objects.all()
        selected_count = 0
        for question in questions:
            answer_text = request.POST.get(f'question_{question.id}', None)
            if answer_text == 'on':
                user = User.objects.get(id=user_id)
                competence = Competence.objects.filter(questions=question).first()
                if competence:
                    selected_questions[question.id] = competence.id
                    selected_count += 1

        request.session['session_selected_questions'] = selected_questions

        return redirect(f'/selected_questions/{user_id}/')

    else:
        questions = Question.objects.all()
        return render(request, 'questions.html', {'questions': questions})


def selected_questions(request, user_id):
    if request.method == 'POST':
        return redirect(f'/results/{user_id}/')

    session_selected_questions = request.session.get('session_selected_questions', {})

    ssq = session_selected_questions.keys()
    session_selected_questions = []

    for id in ssq:
        question = Question.objects.get(id=id)
        session_selected_questions.append(question)

    return render(request, 'selected_questions.html',
                  {'session_selected_questions': session_selected_questions})


def results(request, user_id):
    user = User.objects.get(id=user_id)
    user_answers = UserAnswer.objects.get(user=user)
    session_selected_questions = request.session.get('session_selected_questions', {})
   # group_results = user_answers.values('user__chosen_group').annotate(total_score=Sum('competence'))

    return render(request, 'results.html', {
        'groups': Group.objects.all(),
        'answers': user_answers,
        'ssq':session_selected_questions
       # 'group_results': group_results,
    })

