from typing import Any
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from .forms import *

from .models import *

import logging

logger = logging.getLogger(__name__)

class NewsHome(ListView):
    paginate_by = 10
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

    # .select_related('cat')
    # select_related(key) – «жадная» загрузка связанных данных по внешнему ключу key, который имеет тип ForeignKey;
    # prefetch_related(key) – «жадная» загрузка связанных данных по внешнему ключу key, который имеет тип ManyToManyField.
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('cat')

class AboutView(ListView):
    model = About
    template_name = 'newsapp/about.html'
    context_object_name = 'content'
    extra_context = {'title': 'О сайте'}

    def get_queryset(self):
        return About.objects.filter(is_published=True)

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'newsapp/addpage.html'
    # без этого будет перенаправление по get_absolute_url модели
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = request.user      
        logger.info(f"addpage {user.get_username()} {user.email} title: {request.POST.__getitem__('title')}")
        return super().post(request, *args, **kwargs)

class ShowContact(ListView):
    model = Contact
    template_name = 'newsapp/contacts.html'
    context_object_name = 'contacts'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context

class ShowPost(FormMixin, DetailView):
    model = News
    template_name = 'newsapp/post.html'
    # класс DetailView по умолчанию пытается выбрать из указанной модели запись, используя атрибут pk или slug
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg ='pk' ('post_pk')
    context_object_name = 'post'
    form_class = AddCommentForm
    success_msg = 'Комментарий успешно создан'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'post_slug':self.get_object().slug})

    def post(self, request, *args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
        
    def form_valid(self, form):
        comment = Comment(news = self.get_object(),
                          author = self.request.user,
                          comment = form.cleaned_data['comment'],)
        comment.save()
        messages.success(self.request, self.success_msg)
        logger.info(f"addcomment news: {comment.news} user: {comment.author}")
        return super().form_valid(form)

class NewsCategory(ListView):
    paginate_by = 4
    model = News
    template_name = 'newsapp/index.html'
    context_object_name = 'posts'
    # # для вызова 404 если список пуст
    # allow_empty = False
 
    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        context['title'] = 'Категория - ' + cat.name
        context['cat_selected'] = cat.id
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
