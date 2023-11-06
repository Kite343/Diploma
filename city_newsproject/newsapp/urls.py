from django.urls import path, re_path

from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', NewsHome.as_view(), name='home'),
    path('about/', about, name='about'),
    # path('addpage/', addpage, name='add_page'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    # path('login/', login, name='login'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LoginUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('post/<slug:post_slug>/', show_post, name='post'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', show_category, name='category'),
    path('category/<slug:cat_slug>/', NewsCategory.as_view(), name='category'),
    
]