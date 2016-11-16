from django import template
from tutorial_app.models import Category

#Creates registry of custom work
register = template.Library()

@register.inclusion_tag('cat.html')
def get_category_list(cat=None):
	return {'cats':Category.objects.all(), 'act_cat':cat}

@register.filter(name='addcls')
def adcls(value, arg):
	return value.as_widget(attrs={'class':arg})






















