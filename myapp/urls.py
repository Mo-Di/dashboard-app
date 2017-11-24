from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'myapp/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    # url(r'^accounts/profile/', views.home, name='home'),
    url(r'^query/$', views.query, name='query'),
    url(r'^edit_product/$', views.edit_product, name='edit_product'),
    url(r'^create_product/$', views.create_product, name="create_product"),
    url(r'^delete/$', views.delete, name='delete')
]

