from django.urls import path

from .forms import quizCreatorView1, quizCreatorView2
from .views import ApplicationWizardView, FORMS, successful, quizSelector, quiz, quizState

urlpatterns = [
    path('quizcreator/', ApplicationWizardView.as_view(FORMS)),
    path('quizselector/', quizSelector, name="Selector"),
    path('quizstate/', quizState, name="State"),
    # path('quizcreator/', views.quizCreator, name="Creator"),
    path('successfull/', successful, name="Successful"),
    path('quiz/<int:quiz_id>/', quiz, name="Quiz"),
    # path('evaluationresult/<int:quiz_id>/', views.quizResult, name="Quiz Result"),
]