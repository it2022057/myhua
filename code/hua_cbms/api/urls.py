from django.urls import path
from rest_framework.authtoken import views

from .views import StaffMemberApiView, SubjectApiView, MeetingApiView, SubjectNextIndexApiView, MeetingNextIndexApiView

app_name = 'api'
urlpatterns = [
    # Get requests for model objects
    path('staff/', StaffMemberApiView.as_view()),
    path('subjects/', SubjectApiView.as_view()),
    path('meetings/', MeetingApiView.as_view()),

    # Request to the view using form data or JSON,
    # that will return a JSON response when valid username and password fields are POSTed
    path('auth/', views.obtain_auth_token),

    # URLs for next-index endpoint
    path('subjects/next-index/', SubjectNextIndexApiView.as_view(), name='next_subject_index'),
    path('meetings/next-index/', MeetingNextIndexApiView.as_view(), name='next_meeting_index')
]
