from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Extend default UserAdmin. Fields left as default for now.
    pass
from django.contrib import admin

# Register your models here.
