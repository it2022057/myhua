from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name="index"),
    path('logout', views.logout_view, name='logout'),

    path('signup/<str:token>', views.signup, name='signup'),
    path('signupsuccess', views.signup_success, name='signup_success'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('password/change', views.password_change, name='password_change'),
    path('password/reset/info', views.password_reset_choice, name='password_reset_choice'),
    path('password/forgot', views.forgot_password, name='forgot_password'),
    path('password/token/<str:token>', views.password_token, name='password_token'),

    # URLs for Secretary CRUD for StaffMembers
    path('sec/staff', views.SecListStaffMember.as_view(), name='sec_list_staff_members'),
    path('sec/staff/<int:pk>', views.SecUpdateStaffMember.as_view(), name='sec_update_staff_member'),
    path('sec/staff/<int:pk>/delete', views.SecDeleteStaffMember.as_view(), name='sec_delete_staff_member'),
    path('sec/staff/new', views.SecCreateStaffMember.as_view(), name='sec_create_staff_member'),

    # URLs for customizing/listing a Collective Body's Participants
    path('sec/collectivebody/<int:pk>/participants', views.SecListParticipants.as_view(), name='sec_list_participants'),
    path('sec/collectivebody/<int:pk>', views.SecUpdateParticipants.as_view(),
         name='sec_update_participants'),

    # URLs for Secretary RUD for user's PersonalInfo
    path('sec/staff/<int:pk>/personal-info', views.SecPersonalInfoOverviewList.as_view(), name='sec_personal_info_overview'),
    path('sec/staff/<int:pk>/personal-info/<int:pi_pk>', views.SecUpdatePersonalInfo.as_view(), name='sec_update_personal_info'),
    path('sec/staff/<int:pk>/personal-info/<int:pi_pk>/delete', views.SecDeleteStaffMember.as_view(), name='sec_delete_personal_info'),

    # URL for Applicant autocomplete
    path('applicant/autocomplete', views.ApplicantAutocomplete.as_view(), name='applicant-autocomplete'),
    # URL for StaffMember autocomplete
    path('staff/autocomplete', views.StaffMemberAutocomplete.as_view(), name='staff-autocomplete'),
    # URL for Participant (StaffMember) autocomplete
    path('participant/autocomplete', views.ParticipantAutocomplete.as_view(), name='participant-autocomplete'),
    # URL for Secretariat autocomplete
    path('sec/autocomplete', views.SecretariatAutocomplete.as_view(), name='sec-autocomplete')

]