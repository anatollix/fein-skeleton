from django.conf import settings
from feincms.views.cbv.views import Handler


class LocaleHandler(Handler):

    @property
    def object(self):
        return self.get_object()

    def dispatch(self, request, *args, **kwargs):
        if settings.USE_I18N:
            if request.path != request.path_info:
                request.path_info = request.path
        return super(LocaleHandler, self).handler(request, *args, **kwargs)
