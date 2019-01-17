from django.contrib import admin
from .models import AuditProcess,CaseType,User,WorkFlow

# Register your models here.

class AuditProcessAdmin(admin.ModelAdmin):
    pass

class CaseTypeAdmin(admin.ModelAdmin):
    list_display = "__all__"


admin.site.register(AuditProcess)
admin.site.register(CaseType)
admin.site.register(User)
admin.site.register(WorkFlow)