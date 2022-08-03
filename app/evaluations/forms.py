from django import forms
from .models import Quiz, QuestionSection, EvaluationProcess
from hr.models import Employee


class invisibleDefaultoptionSelect(forms.Select):
    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if not value:
            option['label'] = ""
            option['attrs']['style'] = "display:none"
        return option

class checkboxStyle(forms.widgets.CheckboxSelectMultiple):
    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if value:
            option['attrs']['class'] = "form-check-input"
        return option

class quizForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), widget=invisibleDefaultoptionSelect())
    question_section = forms.ModelMultipleChoiceField(queryset=QuestionSection.objects.all(), widget=checkboxStyle)
    evaluation_process = forms.ModelChoiceField(queryset=EvaluationProcess.objects.all(), widget=invisibleDefaultoptionSelect())
    class Meta:
        model = Quiz
        fields = ['quiz_type', 'evaluator']
        widgets = {'quiz_type': invisibleDefaultoptionSelect(), 'evaluator': invisibleDefaultoptionSelect()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evaluation_process'].widget.attrs.update({'class': 'form-control'})
        self.fields['employee'].widget.attrs.update({'class': 'form-control'})
        self.fields['evaluator'].widget.attrs.update({'class': 'form-control'})
        self.fields['quiz_type'].widget.attrs.update({'class': 'form-control'})


    # def clean(self, *args, **kwargs):
    #     subject = self.cleaned_data.get("subject")
    #     quiz_type = self.cleaned_data.get("quiz_type")
    #     period = self.cleaned_data.get("period")
    #     try:
    #         quiz = Quiz.objects.get(subject=subject, quiz_type=quiz_type, period=period)
    #     except Quiz.DoesNotExist:
    #         quiz = None
    #     if quiz:
    #         raise forms.ValidationError("Ya existe una encuesta con esos datos.")
    #     return super(quizForm, self).clean(*args, **kwargs)