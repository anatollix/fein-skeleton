from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.content.image.models import ImageContent as ImageContentOld


class ImageContent(ImageContentOld):
    width = models.IntegerField(_('Width'), default=608)

    @property
    def image_size(self):
        return u"%dx999999" % self.width

    class Meta(ImageContentOld.Meta):
        abstract=True
