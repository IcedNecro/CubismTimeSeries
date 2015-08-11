__author__ = 'roman'

from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^login/$', views.render_login_form, name="login"),
    url(r'^register/$', views.render_register_form, name="register"),
    url(r'^logout/$', views.process_logout, name='logout'),
    url(r'^process_reg/$', views.process_registration, name='process_reg'),
    url(r'^process_login/$', views.process_login, name='process_login'),
    url(r'^home/$', views.render_home, name='home'),
    url(r'^recieve_auth/$', views.oauth_autorization, name='credits')

]
