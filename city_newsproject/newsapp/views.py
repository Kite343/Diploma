
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from newsapp.forms import AddPostForm

from .models import *

# def index(request):
#     posts = News.objects.all()

#     context = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
 
#     return render(request, 'newsapp/index.html', context=context)

class NewsHome(ListView):
    model = News
    # фреймворк находит шаблон по умолчанию: newsapp/newsapp_list.html
    # переопределим:
    template_name = 'newsapp/index.html'
    # по умолчанию в шаблон передается object_list
    context_object_name = 'posts'
    # # только статические, неизменямые данные:
    # extra_context = {'title': 'Главная страница'}

    # можно передавать и статические и динамические данные
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        # cat_selected со значением 0 для выбора нужной рубрики
        context['cat_selected'] = 0
        return context
    
    def get_queryset(self):
        return News.objects.filter(is_published=True)

def about(request):
    return render(request, 'newsapp/about.html', {'title': 'О сайте'})
 
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
 
#     return render(request, 'newsapp/addpage.html', {'title': 'Добавление статьи', 'form': form})

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'newsapp/addpage.html'
    # без этого будет перенаправление по get_absolute_url модели
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context
 
def contact(request):
    return HttpResponse("Обратная связь")
 
def login(request):
    return HttpResponse("Авторизация")

# def show_post(request, post_slug):
#     post = get_object_or_404(News, slug=post_slug)
 
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
 
#     return render(request, 'newsapp/post.html', context=context)

class ShowPost(DetailView):
    model = News
    template_name = 'newsapp/post.html'
    # класс DetailView по умолчанию пытается выбрать из указанной модели запись, используя атрибут pk или slug
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg ='pk' ('post_pk')
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        return context

# def show_category(request, cat_slug):
#     cat = get_object_or_404(Category, slug=cat_slug)
#     posts = News.objects.filter(cat_id=cat.id)

#     # if len(posts) == 0:
#     #     raise Http404()
 
#     context = {
#         'posts': posts,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat.id,
#     }
 
#     return render(request, 'newsapp/index.html', context=context)

class NewsCategory(ListView):
    model = News
    template_name = 'newsapp/index.html'
    context_object_name = 'posts'
    # # для вызова 404 если список пуст
    # allow_empty = False
 
    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
    
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Категория - ' + str(context['posts'][0].cat)
    #     context['cat_selected'] = context['posts'][0].cat_id
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.filter(slug=self.kwargs['cat_slug'])
        context['title'] = 'Категория - ' + cat[0].name
        context['cat_selected'] = cat[0].id
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
