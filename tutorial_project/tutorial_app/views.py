from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("AYO MALCOLM YOU THE MAN!")

# Create your views here.

