from django.shortcuts import render
from django.http import HttpResponse
from app.config import load_config


# Create your views here.
def index(request):
    context = {'keys': load_config().keys(), 'length': len(load_config().keys())}
    return render(request, 'index.html', context)


def form(request):
    print(request.GET)
    return HttpResponse(request.GET['name'])
