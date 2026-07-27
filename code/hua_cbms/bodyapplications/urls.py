from django.urls import path

from . import views

app_name = 'bodyapplications'
urlpatterns = [
    # URLs for Secretary RUD for Applications
    path('sec/bodyapplication/<int:pk>', views.SecUpdateApplication.as_view(), name='sec_update_bodyapplication'),
    path('sec/', views.SecMultipleListApplication.as_view(), name='sec_list_bodyapplications'),
    path('sec/bodyapplication/<int:pk>/delete', views.SecDeleteApplication.as_view(), name='sec_delete_bodyapplication'),
    path('sec/bodyapplication/<str:token>/show', views.sec_show_application_via_link, name='sec_show_bodyapplication_from_email_link'),

    # URLs for Applicants and their Applications
    path('applicant/bodyapplication/new/body_pk/<int:pk>', views.ApplicantCreateApplication.as_view(), name='applicant_create_bodyapplication'),
    path('applicant/bodyapplication/<int:pk>', views.ApplicantUpdateApplication.as_view(), name='applicant_update_bodyapplication'),
    path('applicant/', views.ApplicantListApplication.as_view(), name='applicant_list_bodyapplications'),
]