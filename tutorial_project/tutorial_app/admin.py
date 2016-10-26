from django.contrib import admin

# Register your models here.
from models import Category, Page

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)