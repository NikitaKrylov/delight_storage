from django.shortcuts import render
from .models import *
from django.views.generic.list import ListView

# Create your views here.


class IndexImg(ListView):

    model = ImageFile
    template_name = 'images.html'
    context_object_name = 'images'
    paginate_by = 10
