from django.urls import path

from . import views

app_name = 'bodies'
urlpatterns = [
    path('sec/', views.SecListCollectiveBody.as_view(), name='sec_list_collective_body'),

    path('sec/collectivebody/autocomplete', views.SecCollectiveBodyAutoComplete.as_view(), name='collectivebody-autocomplete'),
]