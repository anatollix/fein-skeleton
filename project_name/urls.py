import debug_toolbar
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

from feincms.module.page.sitemap import PageSitemap
from blog.feeds import PostFeed
from blog.sitemap import BlogSitemap

handler404 = '{{ project_name }}.project.views.page_not_found'

sitemaps = {
    'pages': PageSitemap,
    'blog': BlogSitemap,
}

urlpatterns = patterns("",
    url(r'^__debug__/', debug_toolbar.urls),
    url(r'^404/$', handler404),
    url(r'^feed/$', PostFeed()),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^photologue/', include('photologue_extra.urls')),
    url(r'', include('fein_extra.urls')),
) + staticfiles_urlpatterns()


if settings.DEBUG:
    urlpatterns += patterns('', (
        r'^site_media/media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}
        ),
    )
