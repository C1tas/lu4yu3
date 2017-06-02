from django.conf.urls import url
from django.conf import settings
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^#home/$', views.index, name='home'),
]
