from django.contrib import admin
from .models import Task


# This class show you readonly data
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)


admin.site.register(Task, TaskAdmin)
