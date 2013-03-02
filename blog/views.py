from datetime import date

from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from tagging.models import TaggedItem, Tag

from blog.models import Post, Category


def index(request,
          category=None,
          year=None,
          month=None,
          day=None,
          author=None,
          template_name="blog/index.html"):
    posts = Post.objects.published().select_related('user')
    extra_context = {}

    if category:
        category = get_object_or_404(Category, slug=category)
        posts = posts.filter(category=category)
        extra_context.update({'category': category})

    if author:
        author = get_object_or_404(User, username=author)
        posts = posts.filter(user=author)
        extra_context.update({'author': author})

    if year:
        posts = posts.filter(published_on__year=int(year))
        extra_context.update({'drilldown_mode': 'year', 'title': year})
    else:
        year=1

    if month:
        # display month as full word.
        from django.template import defaultfilters
        posts = posts.filter(published_on__month=int(month))
        extra_context.update({
            'drilldown_mode': 'month',
            'title' : defaultfilters.date(date(int(year), int(month), 1), 'E Y')
        })
    else:
        month=1

    if day:
        from django.contrib.humanize.templatetags.humanize import naturalday
        posts = posts.filter(published_on__day=int(day))
        extra_context.update({
            'drilldown_mode': 'day',
            'title' : naturalday(date(int(year), int(month), int(day)))
        })
    else:
        day=1

    tag = request.GET.get('tag', None)

    if tag:
        tag = get_object_or_404(Tag, name=tag)
        posts = TaggedItem.objects.get_by_model(posts, tag)
    
    extra_context.update({
        'date': date(int(year), int(month), int(day)),
        'posts': posts,
        'tag': tag,
    })

    return template_name, extra_context


def detail(request,
           year=None,
           month=None,
           day=None,
           slug=None,
           template_name="blog/detail.html"):
    post = get_object_or_404(
        Post.objects.published(user=request.user).select_related('user'),
        published_on__year=year,
        published_on__month=month,
        published_on__day=day,
        slug=slug,
    )
    if post.status in ['trash', 'draft'] and not request.user.is_authenticated():
        raise Http404
    return template_name, {
        'post': post,
        'date': date(int(year), int(month), int(day)),
    }


def random(request):
    return redirect(Post.objects.published().order_by('?')[0])
