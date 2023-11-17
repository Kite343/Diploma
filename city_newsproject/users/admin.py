from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
 
from users.models import User

class UserExtensionAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'date_birth', 'photo')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'date_birth')
    list_editable = ('email', 'first_name', 'last_name', 'is_staff', 'date_birth', 'photo')
 
# admin.site.register(User, UserAdmin)
admin.site.register(User, UserExtensionAdmin)
 