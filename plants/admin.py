from django.contrib import admin

from .models import Comment, Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_edible", "created_at"]
    list_filter = ["category", "is_edible"]
    search_fields = ["name", "about"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["full_name", "plant", "created_at"]
    list_select_related = ["plant"]  # load each comment's plant in the same query
