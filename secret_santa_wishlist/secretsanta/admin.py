from django.contrib import admin
from .models import User, Group

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users. """
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active'
    ]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for groups. """
    list_display = ('name', 'code', 'admin')  # Display group name, code, and admin in the admin panel
    search_fields = ('name', 'code', 'admin__username')  # Add search capabilities

