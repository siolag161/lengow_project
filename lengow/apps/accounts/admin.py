from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

from authtools.admin import StrippedUserAdmin
from authtools.admin import BASE_FIELDS, DATE_FIELDS, SIMPLE_PERMISSION_FIELDS


admin.site.unregister(Group)


class UserAdmin(StrippedUserAdmin):
    list_display = ('is_active', 'name', 'email', 'date_joined',
                    'last_login', 'is_superuser', 'is_staff')
    list_display_links = ('name', 'email')

    search_fields = ('name', 'email')
    list_filter = ('is_active', 'is_superuser', 'is_staff')

    fieldsets = (
        BASE_FIELDS,
        DATE_FIELDS,
        SIMPLE_PERMISSION_FIELDS,
    )


admin.site.register(User, UserAdmin)
