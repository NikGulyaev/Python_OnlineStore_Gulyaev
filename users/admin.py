from django.contrib import admin #type: ignore
from django.contrib.auth.admin import UserAdmin #type: ignore

from users.models import User

# Register your models here.
admin.site.register(User, UserAdmin)
