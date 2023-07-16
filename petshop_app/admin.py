from django.contrib import admin
from .models import *

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'about', 'price', 'is_published')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'about')

admin.site.register(Items, ItemsAdmin)
admin.site.register(Category, CategoryAdmin)