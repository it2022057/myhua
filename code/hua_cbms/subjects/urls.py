from django.urls import path
from . import views

app_name = 'subjects'
urlpatterns = [
    path('sec/subject/new', views.SecCreateSubject.as_view(), name='sec_create_subject'),
    path('sec/subject/<int:pk>', views.SecUpdateSubject.as_view(), name='sec_update_subject'),
    path('sec/', views.SecListSubject.as_view(), name='sec_list_subject'),
    path('sec/subject/<int:pk>/delete', views.SecDeleteSubject.as_view(), name='sec_delete_subject'),
    #path('sec/subject/<int:pk>/overview', views.SecSubjectOverviewList.as_view(), name='sec_overview_phd_student'),

    # URLs for Secretary autocomplete
    path('sec/subject-type/autocomplete', views.SecSubjectTypeAutoComplete.as_view(), name='subject-type-autocomplete'),
    path('sec/subject-category/autocomplete', views.SecSubjectCategoryAutoComplete.as_view(), name='subject-category-autocomplete'),
]
