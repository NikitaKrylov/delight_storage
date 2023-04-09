from django import template
from django.urls import resolve

register = template.Library()


@register.filter
def is_current_page(request, url):
    return request.path == url


@register.filter
def mark_current_page(request, url: str):
    if request.path == url:
        return '_current'
    return ''


@register.filter(name='trange')
def trange(rangelable):
    return range(rangelable)