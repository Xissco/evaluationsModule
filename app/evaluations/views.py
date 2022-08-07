from django.contrib.auth.models import User
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from formtools.wizard.views import SessionWizardView
# from .models import Evaluation, Quiz, Answer
# from .forms import quizForm
# from hr.models import Employee
from evaluations.forms import quizCreatorView1, quizCreatorView2
from evaluations.models import Evaluation, EvaluationProcess, Quiz, QuizType, QuestionAnswer

FORMS = [("evaluation", quizCreatorView1),
         ("quiz", modelformset_factory(Quiz, form=quizCreatorView2))]

TEMPLATES = {"evaluation": "evaluations/evaluationWizard.html",
             "quiz": "evaluations/quizWizard.html"}


class ApplicationWizardView(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_initial(self, step):
        if step == 'quiz':
            form_class = self.form_list[step]
            evaluation_data = self.storage.get_step_data('evaluation')
            evaluation_process = EvaluationProcess.objects.get(id=int(evaluation_data['evaluation-evaluation_process']))
            quiz_type_len = len(evaluation_process.quiz_type.all())
            form_class.extra = quiz_type_len
        return self.initial_dict.get(step, {})

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'quiz':
            evaluation_data = self.storage.get_step_data('evaluation')
            evaluation_process = EvaluationProcess.objects.get(id=int(evaluation_data['evaluation-evaluation_process']))
            quiz_type = evaluation_process.quiz_type.all()
            context.update({'quiz_types': quiz_type})
        return context

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        evaluation_process = form_data.pop(0)
        print(evaluation_process)
        print(form_data)
        evaluation = Evaluation(evaluation_process=evaluation_process['evaluation_process'],
                                evaluated=evaluation_process['evaluated'])
        evaluation.save()
        for evaluator in form_data.pop(0):
            quiz_type = QuizType.objects.get(id=evaluator['category'])
            quiz = Quiz(evaluator=evaluator['evaluator'], quiz_state='1', quiz_type=quiz_type, evaluation=evaluation)
            quiz.save()
            for category in quiz_type.question_category.all():
                for section in category.question_section.all():
                    for question in section.question.all():
                        question_answer = QuestionAnswer(quiz=quiz, question=question)
                        question_answer.save()
        return HttpResponseRedirect('/evaluations/successfull')


def successful(request):
    return render(request, 'evaluations/successfull.html')
# Create your views here.
# def quizSelector(request):
#     if not request.user.is_authenticated: return redirect('/')
#     evaluator = Employee.objects.get(user=request.user)
#     quizes = Quiz.objects.filter(evaluator=evaluator)
#     pendings = len(Quiz.objects.filter(evaluator=evaluator).filter(quiz_state=1))
#     context = {'quizes': quizes, 'pendings': pendings}
#     return render(request, 'evaluations/quizSelector.html', context)
#
#
# def quizState(request):
#     if not request.user.is_authenticated: return redirect('/')
#     if not request.user.is_staff: return redirect('/')
#     evaluations = Evaluation.objects.all()
#     pendings = len(Quiz.objects.all().filter(quiz_state=1))
#     context = {'evaluations': evaluations, 'pendings': pendings}
#     return render(request, 'evaluations/quizState.html', context)
#
#
# def quiz(request, quiz_id):
#     if not request.user.is_authenticated: return redirect('/')
#     quiz = Quiz.objects.get(id=quiz_id)
#     if quiz.quiz_state == '2' or quiz.evaluator.user != request.user:
#         return redirect('/error')
#     if request.method == 'POST':
#         keys = [key for key, value in request.POST.items() if 'csrf' not in key]
#         quizid = request.POST.get(keys.pop(0))
#         quizScore = 0
#         while len(keys):
#             answerValue = int(request.POST.get(keys.pop(0)))
#             quizScore += answerValue
#             answer = Answer(id=request.POST.get(keys.pop(0)), value=answerValue)
#             answer.save(update_fields=["value"])
#         quiz = Quiz.objects.get(id=quizid)
#         quiz.quiz_state = 2
#         quiz.score = quizScore * 50 / 12.0
#         quiz.save(update_fields=["quiz_state", "score"])
#         pendingQuiz = False
#         quizes = quiz.evaluation.quizes.all()
#         for quiz in quizes:
#             if quiz.getState == 'Pendiente':
#                 pendingQuiz = True
#                 break
#         totalScore = 0
#         if not pendingQuiz:
#             for quiz in quizes:
#                 totalScore += quiz.score
#             totalScore = totalScore/len(quizes)
#             quiz.evaluation.score = totalScore
#             quiz.evaluation.save(update_fields=["score"])
#         return redirect('/evaluations/quizselector')
#     else:
#         answer = Answer.objects.filter(quiz=quiz)
#         return render(request, 'evaluations/quiz.html', {'quiz': quiz, 'answer': answer})
#
#
# def quizCreator(request):
#     if not request.user.is_authenticated: return redirect('/')
#     if not request.user.is_staff: return redirect('/')
#     form = quizForm(request.POST or None)
#     if form.is_valid():
#         employee = form.cleaned_data.get("employee")
#         evaluator = form.cleaned_data.get("evaluator")
#         quiz_type = form.cleaned_data.get("quiz_type")
#         evaluation_process = form.cleaned_data.get("evaluation_process")
#         evaluation, created = Evaluation.objects.get_or_create(evaluated=employee, evaluation_process=evaluation_process)
#         quiz = Quiz(quiz_type=quiz_type, evaluation=evaluation, evaluator=evaluator, quiz_state=1)
#         quiz.save()
#         for section in form.cleaned_data.get("question_section"):
#             for question in section.question.all():
#                 answer = Answer(quiz=quiz, question=question)
#                 answer.save()
#         return redirect('/evaluations/quizstate')
#     else:
#         return render(request, 'evaluations/quizCreator.html', {'form': form})
#
# def quizResult(request, quiz_id):
#     if not request.user.is_authenticated: return redirect('/')
#     if not request.user.is_staff: return redirect('/')
#     quiz = get_object_or_404(Quiz, id=quiz_id)
#     answer = Answer.objects.filter(quiz=quiz)
#     return render(request, 'evaluations/quizresult.html', {'quiz': quiz, 'answer': answer})
