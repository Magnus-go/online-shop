from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.forms import UserChangeForm, UserCreationForm
from .models import User
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'fullname', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'fullname', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'fullname', 'phone_number', 'password1', 'password2')}),
    )

    search_fields = ('email', 'phone_number')
    ordering = ('fullname',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
