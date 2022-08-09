from django.urls import path

from .forms import quizCreatorView1, quizCreatorView2
from .views import ApplicationWizardView, FORMS, successful, quizSelector, quiz, quizState, quizResult, evaluationChart, evaluationSelector

urlpatterns = [
    path('quizcreator/', ApplicationWizardView.as_view(FORMS)),
    path('quizselector/', quizSelector, name="Selector"),
    path('evaluationselector/', evaluationSelector, name="Ev Selector"),
    path('quizstate/<int:ep_id>/', quizState, name="State"),
    path('evaluationchart/<int:ep_id>', evaluationChart, name="EvaluationChart"),
    path('successfull/', successful, name="Successful"),
    path('quiz/<int:quiz_id>/', quiz, name="Quiz"),
    path('evaluationresult/<int:quiz_id>/', quizResult, name="Quiz Result"),
]