from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^user/(?P<user_i>\d+)/$', views.user),
    url(r'^friends$', views.friends),
    url(r'^add/(?P<user_i>\d+)/$', views.add),
    url(r'^delete/(?P<user_i>\d+)/$', views.delete),
    url(r'^viewfriend/(?P<user_i>\d+)/$', views.viewfriend),

]
