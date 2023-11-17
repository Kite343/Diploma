from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
# from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.views import LoginView
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.contrib import messages

from .forms import *

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
 
# def contact(request):
#     return HttpResponse("Обратная связь")

class ShowContact(ListView):
    model = Contact
    template_name = 'newsapp/contacts.html'
    context_object_name = 'contacts'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context

    # def get_queryset(self):
    #     return News.objects.filter(is_published=True).select_related('cat')
 
# def login(request):
#     return HttpResponse("Авторизация")



# in users
# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'newsapp/login.html'
 
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Авторизация"
#         return context
    
#     def get_success_url(self):
#         return reverse_lazy('home')
    
# def logout_user(request):
#     logout(request)
#     return redirect('login')

# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     # form_class = UserCreationForm
#     template_name = 'newsapp/register.html'
#     success_url = reverse_lazy('login')
 
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Регистрация"
#         return context
    
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')
# in users


# def show_post(request, post_slug):
#     post = get_object_or_404(News, slug=post_slug)
 
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
 
#     return render(request, 'newsapp/post.html', context=context)

# class ShowPost(DetailView):
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
        return super().form_valid(form)
    

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
    paginate_by = 4
    model = News
    template_name = 'newsapp/index.html'
    context_object_name = 'posts'
    # # для вызова 404 если список пуст
    # allow_empty = False
 
    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
    
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Категория - ' + str(context['posts'][0].cat)
    #     context['cat_selected'] = context['posts'][0].cat_id
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # cat = Category.objects.filter(slug=self.kwargs['cat_slug'])
        # context['title'] = 'Категория - ' + cat[0].name
        # context['cat_selected'] = cat[0].id
        
        # cat = Category.objects.filter(slug=self.kwargs['cat_slug']).first()
        cat = Category.objects.get(slug=self.kwargs['cat_slug'])
        context['title'] = 'Категория - ' + cat.name
        context['cat_selected'] = cat.id
        return context


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
