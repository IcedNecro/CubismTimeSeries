from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('auth_module.urls', namespace='auth')),
    url(r'', 'auth_module.views.handle_all')
)
