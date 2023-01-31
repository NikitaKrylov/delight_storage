from django.shortcuts import render


def heandler404(request, exception):
    return render(request, '404.html', status=404)


def heandler500(request, *args, **kwargs):
    return render(request, '500.html', status=500)