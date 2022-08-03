from django.contrib import admin
from .models import EvaluationProcess, Evaluation, Quiz, QuestionCategory, QuestionSection, Question


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


admin.site.register(EvaluationProcess, BaseAdmin)
admin.site.register(QuestionCategory, BaseAdmin)
admin.site.register(QuestionSection, BaseAdmin)
admin.site.register(Question, BaseAdmin)
admin.site.register(Evaluation, BaseAdmin)
admin.site.register(Quiz, BaseAdmin)
