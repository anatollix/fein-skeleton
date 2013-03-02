from django.http import HttpResponsePermanentRedirect


def permanent_redirect_request_processor(page, request):
    target = page.get_redirect_to_target(request)
    if target:
        return HttpResponsePermanentRedirect(target)
