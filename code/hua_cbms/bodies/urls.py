from django.urls import path

from . import views

app_name = 'bodies'
urlpatterns = [
    path('sec/collectivebody/new', views.SecCreateCollectiveBody.as_view(), name='sec_create_collectivebody'),
    path('sec/collectivebody/<int:pk>', views.SecUpdateCollectiveBody.as_view(), name='sec_update_collectivebody'),
    path('sec/', views.SecListCollectiveBody.as_view(), name='sec_list_collectivebody'),
    path('sec/collectivebody/<int:pk>/delete', views.SecDeleteCollectiveBody.as_view(), name='sec_delete_collectivebody'),
    #path('sec/subject/<int:pk>/overview', views.SecSubjectOverviewList.as_view(), name='sec_overview_phd_student'),

    # URL for CollectiveBody autocomplete
    path('sec/collectivebody/autocomplete', views.SecCollectiveBodyAutoComplete.as_view(), name='collectivebody-autocomplete'),
]