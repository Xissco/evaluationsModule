from django.contrib import admin
from .models import Job, Manager, Department, Employee


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


admin.site.register(Job, BaseAdmin)
admin.site.register(Manager, BaseAdmin)
admin.site.register(Department, BaseAdmin)
admin.site.register(Employee, BaseAdmin)
