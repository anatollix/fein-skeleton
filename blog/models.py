from datetime import datetime

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from feincms.models import Base
from feincms.content.richtext.models import RichTextContent
from feincms.content.video.models import VideoContent

from tagging.fields import TagField

from fein_extra.models import ImageContent
from photologue_extra.models import PhotoContent, GalleryContent


STATUS_CHOICES = (
    ('publish', _('Publish')),
    ('draft', _('Draft')),
    ('future', _('Future')),
    ('trash', _('Trash')),
)

COMMENT_STATUS_CHOICES = (
    ('open', _('Open')),
    ('closed', _('Closed')),
)


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)
    order = models.IntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('order', )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from feincms.content.application.models import app_reverse
        return app_reverse('blog_category_list', 'blog.urls', args=[self.slug])


class PostManager(models.Manager):
    def published(self, user=None):
        if user and user.is_staff:
            return self.all()
        now = datetime.now()
        return self.exclude(status__in=['draft', 'trash']).filter(published_on__lt=now)


class Post(Base):
    user = models.ForeignKey(
        'auth.User',
        blank=True,
        null=True,
        verbose_name=_('author')
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        unique_for_date='published_on', #needs a concrete date in the field published_on.
        help_text='This is used for the generated navigation, too.'
    )
    slug = models.SlugField(_('slug'), max_length=255)
    excerpt = models.TextField(_('excerpt'), default='', blank=True, help_text=_("""
    A condensed description of your blog post,
    is displayed at a blog index page instead of the full post.
    Should contain HTML. If empty, the full post will be displayed.
    """))
    meta_description = models.TextField(_('meta description'), default='', blank=True)
    meta_keywords = models.TextField(_('meta keywords'), default='', blank=True)
    category = models.ForeignKey(Category, verbose_name=_('category'))
    status = models.CharField(
        _('status'),
        max_length=25,
        choices=STATUS_CHOICES,
        default='publish',
        db_index=True
    )
    comment_status = models.CharField(
        _('comment status'),
        max_length=25,
        choices=COMMENT_STATUS_CHOICES,
        default='open',
        db_index=True
    )
    published_on = models.DateTimeField(
        _('published on'),
        blank=True,
        null=True,
        default=datetime.now
    )

    last_changed = models.DateTimeField(
        _('last changed'),
        auto_now=True,
        editable=False
    )

    is_featured = models.BooleanField(
        _('is featured'),
        default=False,
        blank=True,
        db_index=True
    )

    tags = TagField(
        _('tags'),
        max_length=255,
        default="",
        blank=True)

    objects = PostManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        get_latest_by = 'published_on'
        ordering = ['-published_on']

    def __unicode__(self):
        return self.title

    @property
    def publication_date(self):
        return self.published_on

    def get_absolute_url(self):
        entry_dict = {'year': "%04d" %self.published_on.year,
                      'month': "%02d" %self.published_on.month,
                      'day': "%02d" %self.published_on.day,
                      'slug': self.slug}
        from feincms.content.application.models import app_reverse
        url = app_reverse('blog_post', 'blog.urls', kwargs=entry_dict)
        if settings.USE_I18N:
            # terrible hack to undo what locale url does
            return '/' + url.split('/', 2)[2]
        return url


if settings.USE_I18N:
    Post.register_extensions(
        'feincms.module.extensions.translations',
    )

Post.register_regions(
    ('main', _('Main content area')),
)

RichTextContent = Post.create_content_type(RichTextContent)
Post.create_content_type(ImageContent, POSITION_CHOICES=(
    ('block', _('block')),
    ('max', _('max')),
    ('left', _('left')),
    ('right', _('right')),
))
VideoContent = Post.create_content_type(VideoContent)
Post.create_content_type(PhotoContent)
Post.create_content_type(GalleryContent, regions=('main',))
