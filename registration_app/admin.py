"""Django admin configuration for registration app."""

from django.contrib import admin
from registration_app.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for User model.

    Displays and manages user accounts with email and username fields.
    Provides search and filtering capabilities for easier management.
    """
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    ordering = ('-id',)
    readonly_fields = ('id',)
