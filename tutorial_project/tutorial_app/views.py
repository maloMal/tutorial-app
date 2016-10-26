from django.shortcuts import render

from django.http import HttpResponse

from models import Category, Page

def index(request):
	category_list = Category.objects.order_by('-likes')
	context_dict = {}
	context_dict['categories'] = category_list
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list
	return render(request, 'index.html', context_dict)

def about(request):
	return HttpResponse("WE LIT!")

def category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)

		context_dict['category'] = category
		context_dict['pages'] = pages

	except Category.DoesNotExist:
		pass

	return render(request, 'category.html', context_dict)
# Create your views here.

