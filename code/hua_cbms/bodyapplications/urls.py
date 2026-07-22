from django.urls import path

from . import views

app_name = 'bodyapplications'
urlpatterns = [
    # URLs for Secretary RUD for Applications
    path('sec/bodyapplication/<int:pk>', views.SecUpdateApplication.as_view(), name='sec_update_bodyapplication'),
    path('sec/', views.SecListApplication.as_view(), name='sec_list_bodyapplications'),
    path('sec/bodyapplication/<int:pk>/delete', views.SecDeleteApplication.as_view(), name='sec_delete_bodyapplication'),
    # path('sec/bodyapplication/<int:pk>/overview', views.SecApplicationOverviewList.as_view(), name='sec_overview_bodyapplication'),

    # URLs for Applicants and their Applications
    path('applicant/bodyapplication/new', views.ApplicantCreateApplication.as_view(), name='applicant_create_bodyapplication'),
    path('applicant/bodyapplication/<int:pk>', views.ApplicantUpdateApplication.as_view(), name='applicant_update_bodyapplication'),
    path('applicant/', views.ApplicantListApplication.as_view(), name='applicant_list_bodyapplications'),
    # path('applicant/bodyapplication/<int:pk>/overview', views.ApplicantApplicationOverviewList.as_view(), name='applicant_overview_bodyapplication'),
]