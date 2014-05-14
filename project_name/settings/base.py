import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

MANAGERS = ADMINS = []

SITE_ID = 1

USE_I18N = True
USE_L10N = USE_I18N

if USE_I18N:
    from localeurl.models import patch_reverse
    patch_reverse()

    LOCALE_PATHS = [
        os.path.join(PROJECT_ROOT, 'locale'),
    ]
    gettext = lambda s: s

    LANGUAGES = (
        ('en', gettext('English')),
        ('ru', gettext('Russian')),
    )

INTERNAL_IPS = ['127.0.0.1']

TIME_ZONE = "America/Los_Angeles"
LANGUAGE_CODE = "en"

INSTALLED_APPS = [
    "feincms",
    "feincms.module.page",
    'feincms.module.medialibrary',
    "{{ project_name }}.project",
    "blog",

    "disqus",
    "pagination",
    "photologue",
    "tagging",
    "mptt",
    "django_extensions",
    "south",
    "debug_toolbar",
    "sorl.thumbnail",
    "gunicorn",
    "compressor",

    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
]

# These are for user-uploaded content.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")
MEDIA_URL = "/site_media/media/"

# These are for site static media (e.g. CSS and JS)
# This one is where static content is collected to.
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")
STATIC_URL = "/site_media/static/"
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder',
]

# Template stuff
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "{{ project_name }}.project.context_processors.site",
    "{{ project_name }}.project.context_processors.debug",
]

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

ROOT_URLCONF = "{{ project_name }}.urls"

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
]

if USE_I18N:
    MIDDLEWARE_CLASSES = ['localeurl.middleware.LocaleURLMiddleware'] + MIDDLEWARE_CLASSES

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "include_html": True,
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False

BLOG_TITLE = '{{ project_name }}'
BLOG_DESCRIPTION = ''

from urlparse import urljoin
FEINCMS_RICHTEXT_INIT_TEMPLATE = "admin/content/richtext/init_ckeditor_custom.html"
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'CKEDITOR_JS_URL': urljoin(STATIC_URL, 'ckeditor/ckeditor.js'),
}
FEINCMS_REVERSE_MONKEY_PATCH = False
FEINCMS_FRONTEND_EDITING = True

DISQUS_API_KEY = ''
DISQUS_WEBSITE_SHORTNAME = '{{ project_name }}'

if USE_I18N:
    INSTALLED_APPS.append("localeurl")
    ABSOLUTE_URL_OVERRIDES = {
        'page.page': lambda page: page._cached_url,
    }
