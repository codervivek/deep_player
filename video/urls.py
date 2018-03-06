from django.conf.urls import url

from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^video/(?P<pk>\d+)$', views.VideoDetailView.as_view(), name='video-detail'),
    url(r'^upload/$', views.fileupload, name='upload'),
    url(r'^my_videos/$', views.my_videos, name='my_videos'),
    url(r'^search/$', views.SearchListView.as_view(), name='search_list_view'),
    url(r'^videos/$', views.VideoListView.as_view(), name='video_list'),
    url(r'^scene/$', views.sceneSearch, name='sceneSearch'),
    url(r'^info/(?P<pk>\d+)/(?P<time>\d+)$', views.info, name='info'),
    url(r'^uploadvideo/$', views.uploadvideo, name='uploadvideo'),
    url(r'^luis/$', views.luis, name='luis'),
]