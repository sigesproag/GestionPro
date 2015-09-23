from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from . import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('inicio.urls')),
    url(r'^', include('usuario.urls')),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
