from django.urls import path

from . import views

app_name = 'bodies'
urlpatterns = [
    # URLs for Secretary CRUD for collective bodies
    path('sec/collectivebody/new', views.SecCreateCollectiveBody.as_view(), name='sec_create_collectivebody'),
    path('sec/collectivebody/<int:pk>', views.SecUpdateCollectiveBody.as_view(), name='sec_update_collectivebody'),
    path('sec/', views.SecListCollectiveBody.as_view(), name='sec_list_collectivebodies'),
    path('sec/collectivebody/<int:pk>/delete', views.SecDeleteCollectiveBody.as_view(), name='sec_delete_collectivebody'),

    # URL for Secretary for displaying the collective body overview (its subjects, decisions, meetings, etc.)
    path('sec/collectivebody/<int:pk>/overview', views.SecCollectiveBodyOverviewList.as_view(), name='sec_overview_collectivebody'),

    # URL for collective body autocomplete
    path('sec/collectivebody/autocomplete', views.SecCollectiveBodyAutoComplete.as_view(), name='collectivebody-autocomplete'),

    # URLs for Staff Member
    path('staff/', views.StaffListCollectiveBody.as_view(), name='staff_list_collectivebodies'),
    path('staff/collectivebody/<int:pk>/overview', views.StaffCollectiveBodyOverviewList.as_view(), name='staff_overview_collectivebody'),
    # Secure URL for viewing a collective body through a signed email + collective_body_pk token
    path('staff/collectivebody/<str:token>/show', views.staff_show_collectivebody_via_link, name='staff_show_collectivebody_from_email_link'),

    # URL for Applicant for showing available collective bodies
    path('applicant/', views.ApplicantListCollectiveBody.as_view(), name='applicant_list_collectivebodies'),
]