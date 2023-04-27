from functools import wraps

from django.http import Http404
from django.shortcuts import redirect


def ajax_require(function):

    def wrapper(request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return function(request, *args, **kwargs)
        raise Http404()

    return wrapper
