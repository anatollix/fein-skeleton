from django.conf import settings
from feincms.views.cbv.views import Handler


class LocaleHandler(Handler):

    def get_object(self):
        if self.args:
            self.args = tuple(list(self.args)[1:])
        return super(LocaleHandler, self).get_object()

    def dispatch(self, request, *args, **kwargs):
        if settings.USE_I18N:
            if request.path != request.path_info:
                request.path_info = request.path
        return super(LocaleHandler, self).dispatch(request, *args, **kwargs)
