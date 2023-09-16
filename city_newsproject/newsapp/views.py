
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from newsapp.forms import AddPostForm

from .models import *

def index(request):
    posts = News.objects.all()

    context = {
        'posts': posts,
        'title': 'Главная страница',
        'cat_selected': 0,
    }
 
    return render(request, 'newsapp/index.html', context=context)

def about(request):
    return render(request, 'newsapp/about.html', {'title': 'О сайте'})
 
def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
 
    return render(request, 'newsapp/addpage.html', {'title': 'Добавление статьи', 'form': form})
 
def contact(request):
    return HttpResponse("Обратная связь")
 
def login(request):
    return HttpResponse("Авторизация")

def show_post(request, post_slug):
    post = get_object_or_404(News, slug=post_slug)
 
    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
    }
 
    return render(request, 'newsapp/post.html', context=context)

def show_category(request, cat_slug):
    cat = get_object_or_404(Category, slug=cat_slug)
    posts = News.objects.filter(cat_id=cat.id)

    # if len(posts) == 0:
    #     raise Http404()
 
    context = {
        'posts': posts,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat.id,
    }
 
    return render(request, 'newsapp/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
