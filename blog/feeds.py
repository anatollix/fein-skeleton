from django.conf import settings
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site

from blog.models import Post

from BeautifulSoup import BeautifulSoup

class PostFeed(Feed):
    title = settings.BLOG_TITLE
    link = ''
    description = settings.BLOG_DESCRIPTION
    
    def items(self):
        return Post.objects.published().order_by('-published_on')[:10]
        
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        content = u''.join(c.render() for c in item.content.main)
        soup = BeautifulSoup(content)
        site = Site.objects.get_current()
        for link in soup.findAll('a'):
            if link['href'].startswith('/'):
                link['href'] = 'http://'+site.domain+link['href'] 
        for img in soup.findAll('img'):
            if img['src'].startswith('/'):
                img['src'] = 'http://'+site.domain+img['src'] 
        return soup
