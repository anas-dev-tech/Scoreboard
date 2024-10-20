from django.contrib import admin
from .models import CategorizedTag, TagCategory
from django.contrib import admin
from taggit.models import Tag



@admin.register(CategorizedTag)
class CategorizedTagAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category__name']
    list_display = ['name', 'category']



@admin.register(TagCategory)
class TagCategoryAdmin(admin.ModelAdmin):
    '''Admin View for TagCategory'''

    list_display = ('name',)
    
    












admin.site.unregister(Tag)

