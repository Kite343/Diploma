from django import template
from newsapp.models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

register = template.Library()

title_news = 'Анк-Морпорк TIMES'

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Контакты", 'url_name': 'contact'},
        ]

@register.inclusion_tag('newsapp/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
 
    return {"cats": cats, "cat_selected": cat_selected}

@register.inclusion_tag('newsapp/list_menu.html', takes_context=True)
def show_menu(context):    
    request = context['request']
    user_menu = menu.copy()
    if not request.user.is_authenticated or not request.user.is_staff:
        user_menu.pop(1)
    context['menu'] = user_menu
    context['title_news'] = title_news
    return context
 
@register.inclusion_tag('newsapp/show_comments.html', takes_context=True)
def show_comments(context):   
    request = context['request']
    post = context['object']
    comments = Comment.objects.filter(news=post)

    paginator = Paginator(comments, 3) 
    page_number = request.GET.get('page')
    context['comments_page_obj'] = paginator.get_page(page_number)
    return context