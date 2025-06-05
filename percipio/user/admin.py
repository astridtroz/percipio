from django.contrib import admin
from .models import Contributor,Provider, MyUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

admin.site.register(Contributor)
admin.site.register(Provider)

class UserModelAdmin(BaseUserAdmin):
    list_display = ["id","email", "name", "user_type", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "user_type"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "user_type", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(MyUser, UserModelAdmin)
