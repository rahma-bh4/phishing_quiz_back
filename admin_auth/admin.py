from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Admin

@admin.register(Admin)
class AdminUserAdmin(UserAdmin):
    model = Admin

    # Champs à afficher lors de la modification d'un utilisateur
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Champs à afficher lors de la création d'un utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Configuration de l'affichage des utilisateurs dans la liste d'administration
    list_display = ('username', 'email', 'name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'name')
    ordering = ('email',)
