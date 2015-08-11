__author__ = 'roman'

from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^units/$', views.get_units, name="units"),
    url(r'^freq/$', views.get_initial_frequency, name='frequency'),
    url(r'^interconnections/$', views.get_available_interconnections, name='intercon')

]
