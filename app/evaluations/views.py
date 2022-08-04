from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Evaluation, Quiz, Answer
from .forms import quizForm
from hr.models import Employee

# Create your views here.
def quizSelector(request):
    evaluator = Employee.objects.get(user=request.user)
    quizes = Quiz.objects.filter(evaluator=evaluator)
    pendings = len(Quiz.objects.filter(evaluator=evaluator).filter(quiz_state=1))
    context = {'quizes': quizes, 'pendings': pendings}
    return render(request, 'evaluations/quizSelector.html', context)


def quizState(request):
    evaluations = Evaluation.objects.all()
    pendings = len(Quiz.objects.all().filter(quiz_state=1))
    context = {'evaluations': evaluations, 'pendings': pendings}
    return render(request, 'evaluations/quizState.html', context)


def quiz(request, quiz_id):
    if request.method == 'POST':
        keys = [key for key, value in request.POST.items() if 'csrf' not in key]
        quiz_id = request.POST.get(keys.pop(0))
        quizScore = 0
        while len(keys):
            answerValue = int(request.POST.get(keys.pop(0)))
            quizScore += answerValue
            answer = Answer(id=request.POST.get(keys.pop(0)), value=answerValue)
            answer.save(update_fields=["value"])
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.quiz_state = 2
        quiz.score = quizScore * 50 / 12.0
        quiz.save(update_fields=["quiz_state", "score"])
        pendingQuiz = False
        quizes = quiz.evaluation.quizes.all()
        for quiz in quizes:
            if quiz.getState == 'Pendiente':
                pendingQuiz = True
                break
        totalScore = 0
        if not pendingQuiz:
            for quiz in quizes:
                totalScore += quiz.score
            totalScore = totalScore/len(quizes)
            quiz.evaluation.score = totalScore
            quiz.evaluation.save(update_fields=["score"])
        return redirect('/evaluations/quizselector')
    else:
        quizes = get_object_or_404(Quiz, id=quiz_id)
        return render(request, 'evaluations/quiz.html', {'quiz': quizes})


def quizCreator(request):
    form = quizForm(request.POST or None)
    if form.is_valid():
        employee = form.cleaned_data.get("employee")
        evaluator = form.cleaned_data.get("evaluator")
        quiz_type = form.cleaned_data.get("quiz_type")
        evaluation_process = form.cleaned_data.get("evaluation_process")
        evaluation, created = Evaluation.objects.get_or_create(evaluated=employee, evaluation_process=evaluation_process)
        quiz = Quiz(quiz_type=quiz_type, evaluation=evaluation, evaluator=evaluator, quiz_state=1)
        quiz.save()
        for section in form.cleaned_data.get("question_section"):
            for question in section.question.all():
                answer = Answer(quiz=quiz, question=question)
                answer.save()
        return redirect('/evaluations/quizstate')
    else:
        return render(request, 'evaluations/quizCreator.html', {'form': form})

def quizResult(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answer = Answer.objects.filter(quiz=quiz)
    # matrix = []
    # categories = QuestionType.objects.all()
    # totals = evaluation.getCategoryScore
    # for category in categories:
    #     for quiz in evaluation.quizes.all():
    #         categoryScore = quiz.getCategoryScore
    #         matrix.append([category.name, quiz.quiz_type.name, quiz.quiz_type.getWeight.filter(question_type=category).first().weight * 100 ,categoryScore[category.name], round(categoryScore[category.name]*20, 2)])
    #     matrix.append([category.name, "Total", "", totals[category.name], round(totals[category.name] * 20, 2)])
    return render(request, 'evaluations/quizresult.html', {'quiz': quiz, 'answer': answer})
