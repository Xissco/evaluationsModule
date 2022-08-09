from django.contrib import admin
from .models import EvaluationProcess, QuizType, QuestionCategory, QuestionSection, Question, AnswerSet, Answer, \
    Evaluation, Quiz, QuestionAnswer, SectionScore, CategoryScore


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class EvaluationInline(admin.TabularInline):
    model = Evaluation
    readonly_fields = ('evaluated', 'score')

class QuizTypeInline(admin.TabularInline):
    model = EvaluationProcess.quiz_type.through
    fields = ['quiz_type_name', 'quiz_type_value']
    readonly_fields = fields

    def quiz_type_name(self, instance):
        return instance.quiztype.name

    def quiz_type_value(self, instance):
        return instance.quiztype.weight

    quiz_type_value.short_description = 'Valor'
    quiz_type_name.short_description = 'Categoria'

class EvaluationProcessAdmin(admin.ModelAdmin):
    filter_horizontal = ("quiz_type",)
    inlines = [QuizTypeInline, EvaluationInline]

class QuestionCategoryInline(admin.TabularInline):
    model = QuizType.question_category.through
    fields = ['question_category_name', 'question_category_value']
    readonly_fields = fields

    def question_category_name(self, instance):
        return instance.questioncategory.name

    def question_category_value(self, instance):
        return instance.questioncategory.value
    question_category_value.short_description = 'Valor'
    question_category_name.short_description = 'Categoria'

class QuizTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ("question_category",)
    inlines = [QuestionCategoryInline]

class QuestionSectionInline(admin.TabularInline):
    model = QuestionCategory.question_section.through
    fields = ['question_section_name', 'question_section_value']
    readonly_fields = fields

    def question_section_name(self, instance):
        print(instance)
        return instance.questionsection.name

    def question_section_value(self, instance):
        return instance.questionsection.value
    question_section_value.short_description = 'Valor'
    question_section_name.short_description = 'Seccion'

class QuestionCaregoryAdmin(admin.ModelAdmin):
    filter_horizontal = ("question_section",)
    inlines = [QuestionSectionInline]

class QuestionInline(admin.TabularInline):
    model = QuestionSection.question.through
    fields = ['question_content', 'question_value']
    readonly_fields = fields

    def question_content(self, instance):
        return instance.question.content

    def question_value(self, instance):
        return instance.question.value
    question_value.short_description = 'question value'
    question_content.short_description = 'question content'

class QuestionSectionAdmin(admin.ModelAdmin):
    filter_horizontal = ("question",)
    inlines = [QuestionInline]

class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer
    readonly_fields = ('question', 'answer')

class ScoreSectionInline(admin.TabularInline):
    model = SectionScore
    # readonly_fields = ('question', 'answer')

class ScoreCategoryInline(admin.TabularInline):
    model = CategoryScore
    # readonly_fields = ('question', 'answer')

class QuizAdmin(admin.ModelAdmin):
    readonly_fields = ('quiz_type', 'evaluation', 'evaluator', 'score', 'created', 'updated')
    inlines = [QuestionAnswerInline, ScoreCategoryInline, ScoreSectionInline]

class QuizInline(admin.TabularInline):
    model = Quiz
    readonly_fields = ('evaluator', 'quiz_state', 'getWeight', 'score', 'getMaxScore', 'quiz_type')

class EvaluationAdmin(admin.ModelAdmin):
    readonly_fields = ('evaluation_process', 'evaluated', 'score', 'created', 'updated')
    inlines = [QuizInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    readonly_fields = ('content', 'value')

class AnswerSetAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class QuestionSectionAdmin(admin.ModelAdmin):
    filter_horizontal = ("question",)
    inlines = [QuestionInline]

admin.site.register(EvaluationProcess, EvaluationProcessAdmin)
admin.site.register(QuizType, QuizTypeAdmin)
admin.site.register(QuestionCategory, QuestionCaregoryAdmin)
admin.site.register(QuestionSection, QuestionSectionAdmin)
admin.site.register(AnswerSet, AnswerSetAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, BaseAdmin)
# admin.site.register(Answer, BaseAdmin)
