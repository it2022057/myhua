from django.urls import path

from . import views

app_name = 'meetings'
urlpatterns = [
    # URLs for Secretary CRUD for Meetings
    path('sec/meeting/new', views.SecCreateMeeting.as_view(), name='sec_create_meeting'),
    path('sec/meeting/<int:pk>', views.SecUpdateMeeting.as_view(), name='sec_update_meeting'),
    path('sec/', views.SecListMeeting.as_view(), name='sec_list_meetings'),
    path('sec/meeting/<int:pk>/delete', views.SecDeleteMeeting.as_view(), name='sec_delete_meeting'),

    # URL for Staff Members stating their absence/presence in Meetings
    path('staff/', views.StaffListMeeting.as_view(), name='staff_list_meetings')
]
