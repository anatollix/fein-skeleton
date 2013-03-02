from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('blog.views',
   url(r'^random/$', 'random', name='blog_random'),
   url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/',
       'detail',
       name='blog_post'),
   url(r'^category/(?P<category>[^/]+)/$', 'index', name='blog_category_list'),
   url(r'^tagged/$', 'index', name='blog_tag_list'),
   url(r'^(category/(?P<category>[^/]+)/)?((?P<year>\d{4})/)?((?P<month>\d{2})/)?((?P<day>\d{2})/)?$', 'index', name='blog_list'),
   url(r'^author/(?P<author>[^/]+)/$', 'index', name='blog_author_list'),
)
