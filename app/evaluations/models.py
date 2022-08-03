from django.db import models
from hr.models import Employee


# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado el', null=True)
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Actualizado el', null=True)

    class Meta:
        abstract = True


class QuestionCategory(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Categoria')

    class Meta:
        verbose_name = "Categoria de Pregunta"
        verbose_name_plural = "Categorias de Preguntas"
        ordering = ["created"]

    def __str__(self):
        return self.name

class QuestionSection(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Seccion')
    question_category = models.ForeignKey(QuestionCategory, verbose_name='', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Seccion de Pregunta"
        verbose_name_plural = "Secciones de Preguntas"
        ordering = ["created"]

    def __str__(self):
        return self.name


class Question(BaseModel):
    content = models.TextField(verbose_name='Enunciado')
    question_section = models.ForeignKey(QuestionSection, verbose_name='Seccion', on_delete=models.CASCADE, related_name='question')

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ["created"]

    def __str__(self):
        return self.content


class EvaluationProcess(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Proceso')
    question_category = models.ManyToManyField(QuestionCategory, verbose_name='Categorias de Preguntas')
    question_section = models.ManyToManyField(QuestionSection, verbose_name='Secciones de Preguntas')
    question = models.ManyToManyField(Question, verbose_name='Preguntas')

    class Meta:
        verbose_name = "Proceso de Evaluación"
        verbose_name_plural = "Procesos de Evaluación"
        ordering = ["created"]

    def __str__(self):
        return self.name


class Evaluation(BaseModel):
    evaluation_process = models.ForeignKey(EvaluationProcess, verbose_name='Procesos de Evaluación', on_delete=models.CASCADE)
    evaluated = models.ForeignKey(Employee, verbose_name='Evaluado', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Total', null=True, blank=True)

    class Meta:
        verbose_name = "Evaluacion"
        verbose_name_plural = "Evaluaciones"
        ordering = ["created"]


class QuizType(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Tipo de Evaluacion")

    class Meta:
        verbose_name = "Tipo de Evaluacion"
        verbose_name_plural = "Tipos de Evaluacion"
        ordering = ["created"]

    def __str__(self):
        return self.name


class Quiz(BaseModel):
    quiz_type = models.ForeignKey(QuizType, verbose_name="Tipo de Evaluacion", on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, verbose_name='Evaluación', on_delete=models.CASCADE)
    evaluator = models.ForeignKey(Employee, verbose_name='Evaluador', on_delete=models.CASCADE)
    quiz_state = models.CharField(max_length=100, choices=(('1', 'Pendiente'), ('2', 'Realizado')), default='1')
    score = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Total')

    class Meta:
        verbose_name = "Encuesta"
        verbose_name_plural = "Encuestas"
        ordering = ["created"]


class Answer(BaseModel):
    quiz = models.ForeignKey(Quiz, verbose_name="Encuesta", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name="Pregunta", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Valor', null=True, blank=True)