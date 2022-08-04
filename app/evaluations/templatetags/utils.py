import decimal

from django import template
from evaluations.models import Answer

register = template.Library()


@register.filter()
def getAnswerValue(answer, question):
    answerDict = {3:'Muy Desarrollado', 2:'Desarrollado', 1:'Poco Desarrollado', 0:'No Desarrollado'}
    answer = answer.get(question=question)
    answerContent = answerDict[answer.value]
    return answerContent

@register.filter()
def getCategoryTotal(quiz, category):
    evaluation_process = quiz.evaluation.evaluation_process
    categoryScore = 0
    for section in evaluation_process.question_section.filter(question_category=category):
        for question in section.question.all():
            answer = Answer.objects.get(quiz=quiz, question=question)
            categoryScore += answer.value
    return categoryScore * decimal.Decimal(25 / 6.0).quantize(decimal.Decimal("0.01"))
