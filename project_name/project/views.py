from django.shortcuts import render
from feincms.module.page.models import Page

def page_not_found(request, template_name='404.html'):
    page = Page.objects.for_request(request)
    return render(request, template_name, {'feincms_page': page})
