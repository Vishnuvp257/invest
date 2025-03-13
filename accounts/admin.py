from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'dob', 'native', 'gender', 'type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'native', 'type')
    list_filter = ('gender', 'type', 'is_staff', 'is_active')

    fieldsets = (
        ('Personal Information', {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'dob', 'native', 'gender', 'type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'dob', 'native', 'gender', 'type', 'is_staff', 'is_active')}
        ),
    )

    def delete_model(self, request, obj):
        """Before deleting the user, delete related admin logs to prevent IntegrityError."""
        LogEntry.objects.filter(user_id=obj.id).delete()  # Delete admin logs first
        obj.delete()  # Now delete the user safely

admin.site.register(CustomUser, CustomUserAdmin)

