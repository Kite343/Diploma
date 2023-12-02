from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # path('', cache_page(60)(NewsHome.as_view()), name='home'),
    path('', NewsHome.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ShowContact.as_view(), name='contact'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', NewsCategory.as_view(), name='category'),
]