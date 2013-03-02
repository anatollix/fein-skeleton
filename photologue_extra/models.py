from django import forms
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from photologue.models import Gallery, Photo


class PhotoContent(models.Model):
    """
    A single photo from a Photologue gallery
    """
    photo = models.ForeignKey(
        Photo,
        verbose_name=_('Photo'),
        related_name="%(app_label)s_%(class)s_related"
    )

    class Meta:
        abstract = True
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def render(self, **kwargs):
        return render_to_string(
            'photologue/photo_content.html',
            {'object': self.photo}
        )


class GalleryContent(models.Model):
     """
     photologue gallery, different kinds depending on templates
     """
     GALLERY_CHOICES = (
         ('gallery_detail', _(u'Gallery')), # gallery with controls
     )
     gallery = models.ForeignKey(
         Gallery,
         verbose_name=_(u'Gallery'),
        related_name="%(app_label)s_%(class)s_related"
     )
     template = models.CharField(
         _(u'Kind'),
         max_length=31,
         choices=GALLERY_CHOICES,
         default='gallery_detail'
     )

     class Meta:
         abstract = True
         verbose_name = _(u'Gallery')
         verbose_name_plural = _(u'Galleries')

     def render(self, **kwargs):
         return render_to_string(
             'photologue/%s.html' % self.template,
             {'object': self.gallery,
              'STATIC_URL': settings.STATIC_URL}
         )
