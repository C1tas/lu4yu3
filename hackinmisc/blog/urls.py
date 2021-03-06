from django.conf.urls import url
from django.conf import settings
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^!home/$', views.HomeView.as_view(), name='home'),
    url(r'^!daily/$', views.DailyView.as_view(), name='daily'),
    url(r'^!publish/$', views.publish_article, name='publish'),
    url(r'^!post/(?P<slug>[\w-]+)/$', views.PostView.as_view(), name='post'),
    url(r'^!api/publish/$', views.api_publish_article, name='api_publish'),
    url(r'^!api/update/$', views.api_update_article, name='api_update'),
]
