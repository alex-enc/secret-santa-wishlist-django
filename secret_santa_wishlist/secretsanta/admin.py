from django.contrib import admin
from .models import User, Group, GroupMember

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
    list_display = ('name', 'code', 'group_type', 'admin')  # Display group name, code, and admin in the admin panel
    search_fields = ('name', 'code', 'group_type', 'admin__username')  # Add search capabilities

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for group members. """
    list_display = ('user', 'group', 'date_joined', 'is_admin')  # Display group name, code, and admin in the admin panel
    search_fields = ('user', 'group', 'date_joined', 'is_admin')  # Add search capabilities
