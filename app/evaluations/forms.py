from django import forms
from .models import Evaluation, Quiz, QuestionSection, EvaluationProcess
from hr.models import Employee


class invisibleDefaultoptionSelect(forms.Select):
    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if not value:
            option['label'] = ""
            option['attrs']['style'] = "display:none"
        return option


class quizCreatorView1(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['evaluation_process', 'evaluated']
        widgets = {'evaluation_process': invisibleDefaultoptionSelect(), 'evaluated': invisibleDefaultoptionSelect()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evaluation_process'].widget.attrs.update({'class': 'form-control'})
        self.fields['evaluated'].widget.attrs.update({'class': 'form-control'})


class quizCreatorView2(forms.ModelForm):
    category = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Quiz
        fields = ['evaluator']
        widgets = {'evaluator': invisibleDefaultoptionSelect()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evaluator'].widget.attrs.update({'class': 'form-control'})


class quizCreatorView3(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

# class quizForm(forms.ModelForm):
#     employee = forms.ModelChoiceField(queryset=Employee.objects.all(), widget=invisibleDefaultoptionSelect())
#     # question_section = forms.ModelMultipleChoiceField(queryset=QuestionSection.objects.all(), widget=checkboxStyle)
#     evaluation_process = forms.ModelChoiceField(queryset=EvaluationProcess.objects.all(), widget=invisibleDefaultoptionSelect())
#     class Meta:
#         model = Quiz
#         fields = ['quiz_type', 'evaluator']
#         widgets = {'quiz_type': invisibleDefaultoptionSelect(), 'evaluator': invisibleDefaultoptionSelect()}
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['evaluation_process'].widget.attrs.update({'class': 'form-control'})
#         self.fields['employee'].widget.attrs.update({'class': 'form-control'})
#         self.fields['evaluator'].widget.attrs.update({'class': 'form-control'})
#         self.fields['quiz_type'].widget.attrs.update({'class': 'form-control'})
