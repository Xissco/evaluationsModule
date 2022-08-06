from django.contrib import admin
from .models import EvaluationProcess, QuizType, QuestionCategory, QuestionSection, Question, AnswerSet, Answer


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

# class AnswerInline(admin.TabularInline):
#     model = Answer
#     readonly_fields = ('question', 'value')
    # exclude = ('question',)

# class QuizAdmin(admin.ModelAdmin):
#     readonly_fields = ('quiz_type', 'evaluation', 'evaluator', 'score', 'created', 'updated')
#     inlines = [AnswerInline]

admin.site.register(EvaluationProcess, BaseAdmin)
admin.site.register(QuizType, BaseAdmin)
admin.site.register(QuestionCategory, BaseAdmin)
admin.site.register(QuestionSection, BaseAdmin)
admin.site.register(Question, BaseAdmin)
admin.site.register(AnswerSet, BaseAdmin)
admin.site.register(Answer, BaseAdmin)

