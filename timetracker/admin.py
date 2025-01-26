from django.contrib import admin
from .models import Task, Team, Category

# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'created_at')
    search_fields = ('name', 'manager__username')
    filter_horizontal = ('members',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'created_at')
    list_filter = ('team',)
    search_fields = ('name', 'team__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'team', 'owner', 'category', 'status', 'start_time', 'end_time', 'duration')
    list_filter = ('status', 'team', 'category')
    search_fields = ('title', 'description', 'owner__username', 'team__name', 'category__name')
    readonly_fields = ('created_at', 'updated_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            if "team" in request.GET:
                team_id = request.GET["team"]
                kwargs["queryset"] = Category.objects.filter(team_id=team_id)
            elif request.POST.get("team"):
                team_id = request.POST.get("team")
                kwargs["queryset"] = Category.objects.filter(team_id=team_id)
            else:
                kwargs["queryset"] = Category.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
