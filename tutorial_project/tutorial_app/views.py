from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from models import Category, Page, UserProfile
from forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.shortcuts import redirect 
from search import run_query

def index(request):
	category_list = Category.objects.order_by('-likes')
	context_dict = {}
	context_dict['categories'] = category_list
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list
	return render(request, 'index.html', context_dict)

def about(request):
	return render(request, 'about.html', {})


def category(request, category_name_slug):
	context_dict = {}
	context_dict['result_list'] = None
	context_dict['query'] = None

	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
			context_dict['result_list'] = result_list
			context_dict['query'] = query
			print result_list

	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)

		context_dict['category'] = category
		context_dict['pages'] = pages

	except Category.DoesNotExist:
		pass

	return render(request, 'category.html', context_dict)

@login_required
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

@login_required
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

def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)

			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES('picture')

			picture.save()

			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request, 'register.html', {'user_form':user_form,
											'profile_form':profile_form,
											'registered':registered})

def user_login(request):	
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse('Youre not welcome here')
		else:
			print "invalid login details: {0}, {1}".format(username, password)
			return HttpResponse('Your login credentials were wrong')
	else:
		return render(request, 'login.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')
# Create your views here.


def track_url(request):
	page_id = None
	url = '/'
	if request.methond == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET('page_id')
			try:
				page = Page.objects.get(id=page_id)
				page.views = page.views + 1
				page.save()
				url = page.url
			except:
				pass
	return redirect(url)
