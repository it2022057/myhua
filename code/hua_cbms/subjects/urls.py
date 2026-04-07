from django.urls import path
from . import views

app_name = 'subjects'
urlpatterns = [
    # URLs for Subjects
    path('sec/subject/new', views.SecCreateSubject.as_view(), name='sec_create_subject'),
    path('sec/subject/<int:pk>', views.SecUpdateSubject.as_view(), name='sec_update_subject'),
    path('sec/', views.SecListSubject.as_view(), name='sec_list_subject'),
    path('sec/subject/<int:pk>/delete', views.SecDeleteSubject.as_view(), name='sec_delete_subject'),
    #path('sec/subject/<int:pk>/overview', views.SecSubjectOverviewList.as_view(), name='sec_overview_phd_student'),

    # URLs for Decisions
    path('sec/decision/new', views.SecCreateDecision.as_view(), name='sec_create_decision'),
    path('sec/decision/<int:pk>', views.SecUpdateDecision.as_view(), name='sec_update_decision'),
    path('sec/decisions', views.SecListDecision.as_view(), name='sec_list_decision'),
    path('sec/decision/<int:pk>/delete', views.SecDeleteDecision.as_view(), name='sec_delete_decision'),

    # URLs for Secretary autocomplete
    path('sec/subject/autocomplete', views.SecSubjectAutoComplete.as_view(), name='subject-autocomplete'),
    path('sec/subject-type/autocomplete', views.SecSubjectTypeAutoComplete.as_view(), name='subject-type-autocomplete'),
    path('sec/subject-category/autocomplete', views.SecSubjectCategoryAutoComplete.as_view(), name='subject-category-autocomplete'),
]
