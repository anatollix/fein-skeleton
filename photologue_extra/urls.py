from photologue.models import Photo

from django.conf.urls import patterns, url
from django.views.generic import DetailView


urlpatterns = patterns("",
    url(r'^photo/(?P<slug>[\-\d\w]+)/$', DetailView.as_view(), {'slug_field': 'title_slug', 'queryset': Photo.objects.filter(is_public=True)}, name='pl-photo'),
)
