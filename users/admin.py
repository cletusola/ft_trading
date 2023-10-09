from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# custom user admin display 
class CustomeUserAdmin(UserAdmin):

    model = CustomUser

    list_display = ['firstname','lastname','username','email','is_active','is_staff','is_superuser','last_login']
    list_display_links = ['firstname','lastname','username','email']
    list_filter = ['email','is_active','is_staff','is_superuser']
    fieldsets = [
        ('Basic Info', {'fields':('firstname','lastname','username','email',)}),
        ('Permissions', {'fields':('is_active','is_staff','is_superuser',
                        'groups','user_permissions')}),
        ('Dates', {'fields': ('last_login',)})
    ]
    ordering = ('email',)
    search_fields = ['firstname','lastname','username','email']

admin.site.register(CustomUser,CustomeUserAdmin)