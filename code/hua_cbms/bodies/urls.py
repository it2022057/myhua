from django.urls import path

from . import views

app_name = 'bodies'
urlpatterns = [
    # URLs for Secretary CRUD for Collective Bodies
    path('sec/collectivebody/new', views.SecCreateCollectiveBody.as_view(), name='sec_create_collectivebody'),
    path('sec/collectivebody/<int:pk>', views.SecUpdateCollectiveBody.as_view(), name='sec_update_collectivebody'),
    path('sec/', views.SecListCollectiveBody.as_view(), name='sec_list_collectivebodies'),
    path('sec/collectivebody/<int:pk>/delete', views.SecDeleteCollectiveBody.as_view(), name='sec_delete_collectivebody'),
    path('sec/collectivebody/<int:pk>/overview', views.SecCollectiveBodyOverviewList.as_view(), name='sec_overview_collectivebody'),
    path('sec/collectivebody/<int:pk>/participants', views.SecUpdateParticipants.as_view(), name='sec_update_collectivebody_participants'),

    # URL for CollectiveBody autocomplete
    path('sec/collectivebody/autocomplete', views.SecCollectiveBodyAutoComplete.as_view(), name='collectivebody-autocomplete'),

    # URLs for Staff Member
    path('staff/', views.StaffListCollectiveBody.as_view(), name="staff_list_collectivebodies"),
    path('staff/collectivebody/<int:pk>/overview', views.StaffCollectiveBodyOverviewList.as_view(), name='staff_overview_collectivebody'),
]