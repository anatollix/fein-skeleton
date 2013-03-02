from django.conf import settings
from django.contrib.sites.models import Site


def site(request):
    result = {
        'SITE': Site.objects.get_current(),
    }
    return result

def debug(request):
    return {
        'DEBUG': settings.DEBUG,
    }
