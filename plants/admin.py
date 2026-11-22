from django.contrib import admin

from .forms import PlantForm
from .models import Comment, Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    form = PlantForm
    list_display = ("name", "category", "is_edible", "created_at")
    list_filter = ("category", "is_edible")
    search_fields = ("name", "about", "used_for")
    readonly_fields = ("created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "plant", "created_at")
    list_select_related = ("plant",)
    search_fields = ("full_name", "content", "plant__name")
    readonly_fields = ("created_at",)
