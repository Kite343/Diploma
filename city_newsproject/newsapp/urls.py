from django.urls import path, re_path
from django.views.decorators.cache import cache_page
# from django.conf.urls import url

from .views import *
# с этим не работает:
# app_name = 'post'

urlpatterns = [
    # path('', index, name='home'),
    # path('', cache_page(60)(NewsHome.as_view()), name='home'),
    path('', NewsHome.as_view(), name='home'),
    path('about/', about, name='about'),
    # path('addpage/', addpage, name='add_page'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    # path('login/', login, name='login'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('post/<slug:post_slug>/', show_post, name='post'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', show_category, name='category'),
    # path('category/<slug:cat_slug>/', cache_page(60)(NewsCategory.as_view()), name='category'),
    path('category/<slug:cat_slug>/', NewsCategory.as_view(), name='category'),
    # path(r'^comment/(?P<article_id>[0-9]+)/$', add_comment, name='add_comment'),
    # re_path(r'^comment/(?P<news_id>[0-9]+)/$', add_comment, name='add_comment'),
    # path('add_comment/<slug:post_slug>/', add_comment, name='add_comment'),
]