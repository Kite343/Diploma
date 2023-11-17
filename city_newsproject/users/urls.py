from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views

app_name = "users"
 
urlpatterns = [
    # path('login/', views.login_user, name='login'),
    path('login/', views.LoginUser.as_view(), name='login'),
    # path('logout/', views.logout_user, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', views.RegisterUser.as_view(), name='register'),
    
    path('profile/', views.ProfileUser.as_view(), name='profile'),

    # path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    # path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-change/done/',
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done"),
]