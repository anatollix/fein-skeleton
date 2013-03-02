SECRET_KEY = "{{ secret_key }}"

import os

from .base import *


DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "dev.db"),
    },
}
