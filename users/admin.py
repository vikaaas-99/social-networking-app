from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "name", "is_active", "is_superuser")

    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "is_superuser")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    search_fields = ("email", "name")
    ordering = ("email",)


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
