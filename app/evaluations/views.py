from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
# from .models import Evaluation, Quiz, QuestionType, Answer
from .forms import quizForm


# Create your views here.
# def quizSelector(request):
#     quizes = Quiz.objects.filter(evaluator=request.user)
#     pendings = len(Quiz.objects.filter(evaluator=request.user).filter(quiz_state=1))
#     context = {'quizes': quizes, 'pendings': pendings}
#     return render(request, 'evaluations/quizSelector.html', context)
#
#
# def quizState(request):
#     evaluations = Evaluation.objects.all()
#     pendings = len(Quiz.objects.all().filter(quiz_state=1))
#     context = {'evaluations': evaluations, 'pendings': pendings}
#     return render(request, 'evaluations/quizState.html', context)
#
#
# def quiz(request, quiz_id):
#     if request.method == 'POST':
#         keys = [key for key, value in request.POST.items() if 'csrf' not in key]
#         quiz_id = request.POST.get(keys.pop(0))
#         while len(keys):
#             answerValue = request.POST.get(keys.pop(0))
#             answer = Answer(id=request.POST.get(keys.pop(0)), value=answerValue)
#             answer.save(update_fields=["value"])
#         quiz = Quiz.objects.filter(id=quiz_id).first()
#         quiz.quiz_state = 2
#         quiz.save(update_fields=["quiz_state"])
#         return redirect('/evaluations/quizselector')
#     else:
#         quizes = get_object_or_404(Quiz, id=quiz_id)
#         return render(request, 'evaluations/quiz.html', {'quiz': quizes})


def quizCreator(request):
    form = quizForm(request.POST or None)
    # if form.is_valid():
    #     subject = form.cleaned_data.get("subject")
    #     evaluator = form.cleaned_data.get("evaluator")
    #     quiz_type = form.cleaned_data.get("quiz_type")
    #     period = form.cleaned_data.get("period")
    #     evaluation, created = Evaluation.objects.get_or_create(subject=subject, period=period)
    #     quiz = Quiz(subject=subject, evaluation=evaluation, evaluator=evaluator, quiz_type=quiz_type, period=period,
    #                 quiz_state=1)
    #     quiz.save()
    #     for section in form.cleaned_data.get("question_sections"):
    #         for question in section.question.all():
    #             answer = Answer(quiz=quiz, question=question)
    #             answer.save()
    #     return redirect('/evaluations/quizstate')
    # else:
    return render(request, 'evaluations/quizCreator.html', {'form': form})

# def evaluationResult(request, evaluation_id):
#     evaluation = get_object_or_404(Evaluation, id=evaluation_id)
#     matrix = []
#     categories = QuestionType.objects.all()
#     totals = evaluation.getCategoryScore
#     for category in categories:
#         for quiz in evaluation.quizes.all():
#             categoryScore = quiz.getCategoryScore
#             matrix.append([category.name, quiz.quiz_type.name, quiz.quiz_type.getWeight.filter(question_type=category).first().weight * 100 ,categoryScore[category.name], round(categoryScore[category.name]*20, 2)])
#         matrix.append([category.name, "Total", "", totals[category.name], round(totals[category.name] * 20, 2)])
#     return render(request, 'evaluations/evaluationresult.html', {'evaluation': evaluation, 'matrix': matrix})
