from django.contrib import admin
from .models import Comment, Plant

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name", "category", "is_edible", "created_at")
    list_filter = ("category", "is_edible")
    search_fields = ("name", "scientific_name", "about", "used_for")
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "plant", "created_at")
    list_filter = ("created_at",)
    search_fields = ("full_name", "content", "plant__name")
