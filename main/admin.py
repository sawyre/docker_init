from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task, Tag


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")

# Registering models in admin panel
@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    pass

class CustomUserAdmin(UserAdmin):
    UserAdmin.list_display += ('role',)
    UserAdmin.list_filter += ('role',)
    UserAdmin.fieldsets[2][1]["fields"] = UserAdmin.fieldsets[2][1]["fields"] + ("role",)

task_manager_admin_site.register(User, CustomUserAdmin)