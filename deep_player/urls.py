
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from video.views import signup,xyz
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('video.urls')),
    url(r'^admin/', admin.site.urls,name='admin'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', signup, name='signup'),
    url(r'^.well-known/acme-challenge/96iA9V5G6KycDIpqxGEwFENJkrrvLz6W7xRUm3_wwek/$',xyz, name='xyz')
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

