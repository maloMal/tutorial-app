from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	context_dict = {'boldmessage':'LOVE THE MONKEYS OR GET SHOT  '}
	return render(request, 'index.html', context_dict)

def about(request):
	return HttpResponse("WE LIT!")

# Create your views here.

