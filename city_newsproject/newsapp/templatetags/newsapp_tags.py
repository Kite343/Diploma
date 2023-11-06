from django import template
from newsapp.models import *

register = template.Library()

title_news = 'Анк-Морпорк TIMES'

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        # {'title': "Войти", 'url_name': 'login'}
        ]

# @register.simple_tag(name='getcats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)

@register.inclusion_tag('newsapp/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
 
    return {"cats": cats, "cat_selected": cat_selected}

# @register.inclusion_tag('newsapp/list_menu.html')
# def show_menu():
#     menu = [{'title': "О сайте", 'url_name': 'about'},
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         {'title': "Войти", 'url_name': 'login'}
#         ]
 
#     return {"menu": menu}

@register.inclusion_tag('newsapp/list_menu.html', takes_context=True)
def show_menu(context):    
    request = context['request']
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(1)
    context['menu'] = user_menu
    context['title_news'] = title_news
    return context
 
    
