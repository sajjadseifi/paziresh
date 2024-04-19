"""
URL configuration for ensaniapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from ensani.views import header_partial_view, header_references_partial_view, footer_partial_view, navbar_partial_view, \
    footer_references_partial_view, panel_home
from ensani_statistics.views import amar_test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('soldiers.urls')),
    path('', include('battalions.urls')),
    path('', include('accounts.urls')),
    path('', panel_home.as_view(), name='home_page'),
    path('test', amar_test, name='amar'),
    re_path(r'^header_partial_view',
            header_partial_view,
            name='header_partial_view'),
    re_path(r'^header_references_partial_view',
            header_references_partial_view,
            name='header_references_partial_view'),
    re_path(r'^footer_partial_view',
            footer_partial_view,
            name='footer_partial_view'),
    re_path(r'^footer_references_partial_view',
            footer_references_partial_view,
            name='footer_references_partial_view'),
    re_path(r'^navbar_partial_view',
            navbar_partial_view,
            name='navbar_partial_view'),
]
# add root static files
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# add media static files
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
