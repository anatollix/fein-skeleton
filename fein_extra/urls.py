from django.conf.urls import patterns, url

from .views import LocaleHandler
handler = LocaleHandler.as_view()


urlpatterns = patterns('',
    url(r'^$', handler, name='feincms_home'),
    url(r'^(.*)/$', handler, name='feincms_handler'),
)
