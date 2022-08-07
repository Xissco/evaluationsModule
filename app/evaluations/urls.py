from django.urls import path

from .forms import quizCreatorView1, quizCreatorView2
from .views import ApplicationWizardView, FORMS, successful

urlpatterns = [
    path('quizcreator/', ApplicationWizardView.as_view(FORMS)),
    # path('quizselector/', views.quizSelector, name="Selector"),
    # path('quizstate/', views.quizState, name="State"),
    # path('quizcreator/', views.quizCreator, name="Creator"),
    path('successfull/', successful, name="Successful"),
    # path('quiz/<int:quiz_id>/', views.quiz, name="Quiz"),
    # path('evaluationresult/<int:quiz_id>/', views.quizResult, name="Quiz Result"),
]