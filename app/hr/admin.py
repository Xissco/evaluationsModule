from django.contrib import admin
from .models import Job, Manager, Department, Employee


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

# class EmployeeAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         job = form.cleaned_data.get("job")
#         manager = False
#         try:
#             manager = Manager.objects.get(job=job)
#         except Manager.DoesNotExist:
#             manager = False
#         if form.cleaned_data.get("isManager") and not manager:
#             Manager.objects.create(job=job)
#         elif not form.cleaned_data.get("isManager") and manager:
#             Manager.objects.get(job=job).delete()
#         return super(EmployeeAdmin, self).save_model(request, obj, form, change)

admin.site.register(Job, BaseAdmin)
admin.site.register(Manager, BaseAdmin)
admin.site.register(Department, BaseAdmin)
admin.site.register(Employee, BaseAdmin)
