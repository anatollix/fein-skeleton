from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.video.models import VideoContent
from feincms.content.application.models import ApplicationContent
from feincms.content.template.models import TemplateContent
from feincms.content.raw.models import RawContent

from photologue_extra.models import PhotoContent, GalleryContent
from fein_extra.models import ImageContent

extensions = [
    'feincms.module.extensions.changedate',
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.titles',
    'feincms.module.page.extensions.navigation',
    'feincms.module.extensions.ct_tracker',
]

if settings.USE_I18N:
    extensions.append('feincms.module.extensions.translations')

Page.register_extensions(
    *extensions
)

Page.register_templates({
    'title': _('Standard template'),
    'path': 'page.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ),
    })

Page.register_templates({
    'title': _('Homepage template'),
    'path': 'homepage.html',
    'regions': (
        ('main', _('Main content area')),
        ),
    })

Page.register_templates({
    'title': _('Blog template'),
    'path': 'blog/base.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ),
    })

PageRichTextContent = Page.create_content_type(RichTextContent, cleanse=False)

Page.create_content_type(TemplateContent)


Page.create_content_type(ImageContent, POSITION_CHOICES=(
    ('block', _('block')),
    ('max', _('max')),
    ('left', _('left')),
    ('right', _('right')),
    ))
Page.create_content_type(VideoContent)

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('blog.urls', _('Blog'), {
        'urls': 'blog.urls',
    }),
))

Page.create_content_type(PhotoContent)
Page.create_content_type(GalleryContent, regions=('main',))
Page.create_content_type(RawContent)

from .request_processors import permanent_redirect_request_processor

Page.register_request_processor(permanent_redirect_request_processor)
