from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado el', null=True)
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Actualizado el', null=True)

    class Meta:
        abstract = True


class Job(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Puesto')

    class Meta:
        verbose_name = "puesto"
        verbose_name_plural = "puestos"
        ordering = ["created"]

    def __str__(self):
        return self.name


class Manager(BaseModel):
    job = models.OneToOneField(Job, verbose_name='Coordinador', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "coordinador"
        verbose_name_plural = "coordinadores"
        ordering = ["created"]

    def __str__(self):
        return self.job.name


class Department(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Departamento')
    manager = models.OneToOneField(Manager, verbose_name='Responsable', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"
        ordering = ["created"]

    def __str__(self):
        return self.name


class Employee(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Nombres')
    lastname = models.CharField(max_length=100, verbose_name='Apellidos')
    employee_id = models.CharField(max_length=10, verbose_name='Cedula')
    hire_date = models.DateField(verbose_name='Fecha de Ingreso')
    job = models.ForeignKey(Job, verbose_name='Puesto', on_delete=models.CASCADE, null=True)
    departament = models.ForeignKey(Department, verbose_name='Departamento', on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "empleado"
        verbose_name_plural = "empleados"
        ordering = ["created"]

    def __str__(self):
        return self.name
