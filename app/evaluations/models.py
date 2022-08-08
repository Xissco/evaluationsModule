from django.db import models
from hr.models import Employee


# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado el', null=True)
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Actualizado el', null=True)

    class Meta:
        abstract = True


class AnswerSet(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    max_value = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Maximo Valor de Respuesta')

    class Meta:
        verbose_name = "Set de Respuesta"
        verbose_name_plural = "Sets de Respuestas"
        ordering = ["created"]

    def __str__(self):
        return self.name

class Answer(BaseModel):
    content = models.TextField(verbose_name="Enunciado")
    value = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Valor', null=True, blank=True)
    answer_set = models.ForeignKey(AnswerSet, verbose_name='Set de Respuesta', on_delete=models.CASCADE, related_name='answer')

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"
        ordering = ["created"]

    def __str__(self):
        return self.content


class Question(BaseModel):
    content = models.TextField(verbose_name='Enunciado')
    value = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Peso', null=True, blank=True)
    answer_set = models.ForeignKey(AnswerSet, verbose_name='Opciones de respuestas', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ["created"]

    def __str__(self):
        return self.content


class QuestionSection(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Seccion')
    value = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Peso', null=True, blank=True)
    question = models.ManyToManyField(Question, verbose_name='Preguntas')

    class Meta:
        verbose_name = "Seccion de Pregunta"
        verbose_name_plural = "Secciones de Preguntas"
        ordering = ["created"]

    def __str__(self):
        return self.name


class QuestionCategory(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Seccion')
    value = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Peso', null=True, blank=True)
    question_section = models.ManyToManyField(QuestionSection, verbose_name='Secciones de Preguntas')

    class Meta:
        verbose_name = "Categoria de Pregunta"
        verbose_name_plural = "Categorias de Preguntas"
        ordering = ["created"]

    def __str__(self):
        return self.name


class QuizType(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Tipo de Encuesta")
    weight = models.DecimalField(max_digits=50, decimal_places=2)
    question_category = models.ManyToManyField(QuestionCategory, verbose_name="Categorias de Preguntas")

    class Meta:
        verbose_name = "Tipo de Encuesta"
        verbose_name_plural = "Tipos de Encuesta"
        ordering = ["created"]

    def __str__(self):
        return self.name


class EvaluationProcess(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Proceso')
    quiz_type = models.ManyToManyField(QuizType, verbose_name='Tipos de Evaluacion')
    max_score = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Nota Maxima')

    class Meta:
        verbose_name = "Proceso de Evaluación"
        verbose_name_plural = "Procesos de Evaluación"
        ordering = ["created"]

    def __str__(self):
        return self.name


class Evaluation(BaseModel):
    evaluation_process = models.ForeignKey(EvaluationProcess, verbose_name="Proceso de Evaluacion", on_delete=models.CASCADE)
    evaluated = models.ForeignKey(Employee, verbose_name="Evaluado", on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Total')

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciónes"
        ordering = ["created"]

    def __str__(self):
        return str(self.evaluation_process) + " - " + str(self.evaluated.name) + " " + str(self.evaluated.lastname)


class Quiz(BaseModel):
    evaluator = models.ForeignKey(Employee, verbose_name='Evaluador', on_delete=models.CASCADE)
    quiz_state = models.CharField(max_length=100, choices=(('1', 'Pendiente'), ('2', 'Realizado')), default='1')
    score = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Total')
    quiz_type = models.ForeignKey(QuizType, verbose_name="Tipo de Evaluacion", on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, verbose_name='Evaluación', on_delete=models.CASCADE, related_name='quizes')

    class Meta:
        verbose_name = "Encuesta"
        verbose_name_plural = "Encuestas"
        ordering = ["created"]

    def __str__(self):
        return str(self.quiz_type) + " - " + str(self.evaluation.evaluated.name) + " " + str(self.evaluation.evaluated.lastname)

    @property
    def getWeight(self):
        return self.quiz_type.weight

    @property
    def getMaxScore(self):
        return self.evaluation.evaluation_process.max_score * self.quiz_type.weight

    @property
    def getState(self):
        return 'Pendiente' if self.quiz_state == "1" else 'Realizado'


class QuestionAnswer(BaseModel):
    quiz = models.ForeignKey(Quiz, verbose_name="Encuesta", on_delete=models.CASCADE, related_name="answer")
    question = models.ForeignKey(Question, verbose_name="Pregunta", on_delete=models.CASCADE, related_name="answer")
    answer = models.ForeignKey(Answer, verbose_name="Respuesta", on_delete=models.CASCADE, null=True, blank=True)