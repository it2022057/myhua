"""
URL configuration for hua_cbms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import media_download

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # Keeping api/ outside i18n_patterns avoids POST requests to not accidentally become GET after redirect
    path('api/', include('api.urls')),
    path('media/<path:path>', media_download, name='media_download')
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('bodies/', include('bodies.urls')),
    path('curricula/', include('curricula.urls')),
    path('meetings/', include('meetings.urls')),
    path('subjects/', include('subjects.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
