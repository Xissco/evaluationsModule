import decimal

from django import template

register = template.Library()


@register.filter()
def getAnswerValue(answer, question):
    answer = answer.get(question=question)
    return answer.answer.content

@register.filter()
def getField(fields, field):
    return fields[field-1]


@register.filter()
def getFieldId(fields, field):
    return fields[field-1].id


@register.filter()
def getQuestionAnswerId(question_answer, question):
    question_answer_id = question_answer.get(question=question)
    return question_answer_id.id

@register.filter()
def getCategoryTotal(quiz, category):
    TWOPLACES = decimal.Decimal(10) ** -2
    categoryScore = 0
    max_get_category_score = 0
    for section in category.question_section.all():
        for question in section.question.all():
            for question_answer in question.answer.filter(quiz=quiz):
                categoryScore += question_answer.answer.value
                max_get_category_score += question_answer.question.answer_set.max_value
    max_print_category_score = category.value * quiz.evaluation.evaluation_process.max_score
    return categoryScore * max_print_category_score / max_get_category_score
