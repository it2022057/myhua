from django.urls import path

from . import views

app_name = 'curricula'
urlpatterns = [
    # URLs for Secretary autocomplete
    path('sec/program/autocomplete', views.SecProgramAutoComplete.as_view(), name='program-autocomplete'),
    path('sec/department/autocomplete', views.SecDepartmentAutoComplete.as_view(), name='department-autocomplete'),
    path('sec/school/autocomplete', views.SecSchoolAutoComplete.as_view(), name='school-autocomplete'),
]