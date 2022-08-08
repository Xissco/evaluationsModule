import decimal

from django import template
from evaluations.models import Answer

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
    for section in category.question_section.all():
        for question in section.question.all():
            for question_answer in question.answer.filter(quiz=quiz):
                categoryScore += question_answer.answer.value
    return (categoryScore * decimal.Decimal(25 / 6.0)).quantize(TWOPLACES)
