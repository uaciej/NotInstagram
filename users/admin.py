from django.contrib import admin
from .models import Account, Tier
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = Account
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'tier')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'tier')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    list_display = ('email', 'is_staff', 'is_active', 'tier',)
    ordering = ('email',)

admin.site.register(Account, CustomUserAdmin)
admin.site.register(Tier)