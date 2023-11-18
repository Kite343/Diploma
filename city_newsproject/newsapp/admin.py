from django.contrib import admin

from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(News, NewsAdmin)

admin.site.register(Category, CategoryAdmin)

@admin.register(Comment)  
class CommentAdmin(admin.ModelAdmin):  
    list_display = ('news', 'author', 'comment', 'time_create')   
    list_filter = ('time_create', ) 
    search_fields = ('news', 'author', 'comment', 'time_create')


@admin.register(Contact)  
class ContactAdmin(admin.ModelAdmin):  
    list_display = ('type_contact', 'contact', )   
    list_filter = ('type_contact', ) 
    search_fields = ('type_contact', 'contact', )

@admin.register(About)  
class AboutAdmin(admin.ModelAdmin):  
    list_display = ('title', 'content', 'photo_1', 'photo_2', 'photo_3',  'is_published', 'position',)
    ordering = ['position']   