from django import forms
from models import Page, Category, UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'password', 'email')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture', 'bio')



class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text='Please enter a category name!')
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Category
		fields = ('name',)
		exclude = ('user',)
class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text='Please enter a page name!')	
	url = forms.URLField(max_length=200, help_text="please enter page URL!")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')


		if url and not url.startswith('http://'):
			url = 'http://'+ url
			cleaned_data['url'] = url
		return cleaned_data
	class Meta:
		model = Page
		exclude = ('category', 'user')
