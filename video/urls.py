from django.conf.urls import url

from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^video/(?P<pk>\d+)$', views.VideoDetailView.as_view(), name='video-detail'),
    url(r'^upload/$', views.fileupload, name='upload'),
    # url(r'^category/$', views.CategoryListView.as_view(), name='cat'),
    # url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post-detail'),
    # url(r'^comment/(?P<pk>\d+)$', views.CommentDetailView.as_view(), name='comment-detail'),
    # url(r'^category/(?P<slug>[^/]+)/$', views.CategoryDetailView.as_view(), name='category-detail'),
    # url(r'^post/create/$', views.PostCreate.as_view(), name='post_create'),
    # url(r'^post/(?P<pk>\d+)/update/$', views.PostUpdate.as_view(), name='post_update'),
    # url(r'^post/(?P<pk>\d+)/delete/$', views.PostDelete.as_view(), name='post_delete'),
    # url(r'^new/category/create/$', views.CategoryCreate.as_view(), name='category_create'),
    # url(r'^category/(?P<pk>\d+)/update/$', views.CategoryUpdate.as_view(), name='category_update'),
    # url(r'^category/(?P<pk>\d+)/delete/$', views.CategoryDelete.as_view(), name='category_delete'),
    # url(r'^comment/create/$', views.CommentCreate.as_view(), name='comment_create'),
    # url(r'^comment/(?P<pk>\d+)/update/$', views.CommentUpdate.as_view(), name='comment_update'),
    # url(r'^comment/(?P<pk>\d+)/delete/$', views.CommentDelete.as_view(), name='comment_delete'),
    # url(r'^search/$', views.SearchListView.as_view(), name='search_list_view'),
]