from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):

    model = User
    add_form = CustomUserCreationForm
    list_display = ['username', 'email', 'role', 'is_staff']

    fieldsets = (*UserAdmin.fieldsets, ('User role', {'fields': ('role',)}))

    add_fieldsets = (*UserAdmin.add_fieldsets, ('Staff', {'fields': ('role',)}))


admin.site.register(User, CustomUserAdmin)
