from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import MyUser,Department
class MyUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(MyUser)
admin.site.register(Department)