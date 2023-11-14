from django import template
from newsapp.models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

register = template.Library()

title_news = 'Анк-Морпорк TIMES'

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        # {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Контакты", 'url_name': 'contact'},
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
    if not request.user.is_authenticated or not request.user.is_staff:
        user_menu.pop(1)
    context['menu'] = user_menu
    context['title_news'] = title_news
    return context
 
# заготовка ?
# @register.inclusion_tag('newsapp/comments_menu.html', takes_context=True)
# def comments_menu(context):    
#     comments = Comments.objects.all()
#     comments['comments'] = comments
#     return context

# заготовка ?
@register.inclusion_tag('newsapp/show_comments.html', takes_context=True)
def show_comments(context):
    # print(context)    
    request = context['request']
    # print(request)
    post = context['object']
    # print(post)
    comments = Comment.objects.filter(news=post)
    # News.objects.filter(is_published=True).select_related('cat')
    # post = get_object_or_404(News, slug=post_slug)

    paginator = Paginator(comments, 3) 
    page_number = request.GET.get('page')
    context['comments'] = paginator.get_page(page_number)
    # context['page_obj'] = paginator.get_page(page_number)
    # context['paginator'] = paginator
    # print(context['comments'])
    

    # context['comments'] = comments

    # for i in comments:
    #     print(i.author)
    #     print(i.comment)
    #     print()
    return context