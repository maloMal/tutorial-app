from django.shortcuts import render
from django.http import HttpResponse
from models import Category, Page
from forms import CategoryForm, PageForm

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
def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else: 
		form = CategoryForm()
	return render(request, 'add_category.html', {'form':form})	
def add_page(request, category_name_slug):
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			if cat: 
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
			else: print form.errors
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {'form': form, 'category': cat, 'slug': category_name_slug}
	return render(request, 'add_page.html', context_dict)



# Create your views here.

