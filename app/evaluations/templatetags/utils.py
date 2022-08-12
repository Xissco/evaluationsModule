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
def getSectionScore(section_scores, section):
    section_score = section_scores.get(question_section=section)
    return section_score.value

@register.filter()
def getCategoryScore(category_scores, category):
    category_score = category_scores.get(question_category=category)
    return category_score.value

@register.filter()
def getMaxCategoryScore(quiz, category):
    return quiz.getCategoryMaxScore(category)

@register.simple_tag
def getSectionScore(quiz, category, section):
    return quiz.getSectionMaxScore(category, section)

@register.filter()
def getMaxQuizScore(quiz):
    return quiz.getQuizMaxScore()