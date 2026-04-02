from django.contrib import admin
from .models import School, Department, StudyProgram, Institution

# Register your models here.

admin.site.register(School)
admin.site.register(Department)
admin.site.register(StudyProgram)
admin.site.register(Institution)

