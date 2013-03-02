from django import template
from django.template.defaultfilters import truncatewords_html
from django.db.models import Count

from blog.models import Post, Category


register = template.Library()


@register.inclusion_tag('blog/latest_posts.html')
def latest_posts(num=3):
    posts = Post.objects.published()[:num]
    return {'posts': posts}


@register.assignment_tag(takes_context=True)
def featured_posts(context, num=6):
    return Post.objects.published().filter(is_featured=True)[:num]


@register.assignment_tag(takes_context=True)
def posts(context):
    return Post.objects.published()


@register.inclusion_tag('blog/categories.html')
def blog_categories():
    categories = Category.objects.annotate(post_count=Count('post')).order_by('order', 'name')
    return {'categories': categories}


@register.assignment_tag(takes_context=True)
def post_image(context, post):
    from feincms.content.image.models import ImageContent
    images = filter(lambda x: isinstance(x, ImageContent), post.content.main)
    if images:
        return images[0]
    return None


@register.assignment_tag(takes_context=True)
def post_excerpt(context, post):
    if post.excerpt:
        return post.excerpt
    from feincms.content.richtext.models import RichTextContent
    text_content = filter(lambda x: isinstance(x, RichTextContent), post.content.main)
    if text_content:
        return truncatewords_html(text_content[0].text, 40)
    return ""
