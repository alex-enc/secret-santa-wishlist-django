from django.contrib import admin
from .models import User, Group, GroupMember, Wishlist, Assignment, WishlistItem

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

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for secret santa assignments. """
    list_display = ('giver', 'receiver', 'group', 'year')  
    search_fields = ('giver', 'receiver', 'group', 'year')  # Add search capabilities

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Wishlists. """
    list_display = ('user', 'group', 'created_at')  
    search_fields = ('user', 'group', 'created_at')  # Add search capabilities
