from django.shortcuts import render
from django.urls import reverse_lazy

from mysite.services import ajax_require
from .services.generation import ContentParser
from mediacore.models import ImageFile
# Create your views here.


# @ajax_require
def get_parsered_image_path(request, *args, **kwargs):
    parser = ContentParser()
    return parser.get(lazy=kwargs.get('lazy', False))


def delete_parsered_image(request, *args, **kwargs):
    pass


