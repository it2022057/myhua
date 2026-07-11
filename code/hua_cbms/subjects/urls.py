from django.urls import path
from . import views

app_name = 'subjects'
urlpatterns = [
    # URLs for Secretary CRUD for Subjects
    path('sec/subject/new', views.SecCreateSubject.as_view(), name='sec_create_subject'),
    path('sec/subject/<int:pk>', views.SecUpdateSubject.as_view(), name='sec_update_subject'),
    path('sec/', views.SecListSubject.as_view(), name='sec_list_subjects'),
    path('sec/subject/<int:pk>/delete', views.SecDeleteSubject.as_view(), name='sec_delete_subject'),
    #path('sec/subject/<int:pk>/overview', views.SecSubjectOverviewList.as_view(), name='sec_overview_phd_student'),

    # URLs for Secretary CRUD for SubjectTypes
    path('sec/subject-type/new', views.SecCreateSubjectType.as_view(), name='sec_create_subject-type'),
    path('sec/subject-type/<int:pk>', views.SecUpdateSubjectType.as_view(), name='sec_update_subject-type'),
    path('sec/subject-types', views.SecListSubjectType.as_view(), name='sec_list_subject-types'),
    path('sec/subject-type/<int:pk>/delete', views.SecDeleteSubjectType.as_view(), name='sec_delete_subject-type'),

    # URLs for Secretary CRUD for SubjectCategories
    path('sec/subject-category/new', views.SecCreateSubjectCategory.as_view(), name='sec_create_subject-category'),
    path('sec/subject-category/<int:pk>', views.SecUpdateSubjectCategory.as_view(), name='sec_update_subject-category'),
    path('sec/subject-categories', views.SecListSubjectCategory.as_view(), name='sec_list_subject-categories'),
    path('sec/subject-category/<int:pk>/delete', views.SecDeleteSubjectCategory.as_view(), name='sec_delete_subject-category'),

    # URLs for Secretary CRUD for Decisions
    path('sec/decision/new', views.SecCreateDecision.as_view(), name='sec_create_decision'),
    path('sec/decision/<int:pk>', views.SecUpdateDecision.as_view(), name='sec_update_decision'),
    path('sec/decisions', views.SecListDecision.as_view(), name='sec_list_decisions'),
    path('sec/decision/<int:pk>/delete', views.SecDeleteDecision.as_view(), name='sec_delete_decision'),

    # URLs for Staff Member
    path('staff/', views.StaffListSubject.as_view(), name='staff_list_subjects'),
    path('staff/decisions', views.StaffListDecision.as_view(), name='staff_list_decisions'),

    # URLs for Secretary autocomplete
    path('sec/subject/autocomplete', views.SecSubjectAutoComplete.as_view(), name='subject-autocomplete'),
    path('sec/subject-type/autocomplete', views.SecSubjectTypeAutoComplete.as_view(), name='subject-type-autocomplete'),
    path('sec/subject-category/autocomplete', views.SecSubjectCategoryAutoComplete.as_view(), name='subject-category-autocomplete'),
]
