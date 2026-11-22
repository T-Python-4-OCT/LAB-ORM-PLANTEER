from django.contrib import admin

from .models import Comment, Contact, Plant


class CommentInline(admin.TabularInline):
    """A plant's comments, shown inside the plant's admin page."""
    model = Comment
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_edible", "created_at")
    list_filter = ("category", "is_edible")
    search_fields = ("name", "about", "used_for")
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "plant", "created_at")
    search_fields = ("full_name", "content", "plant__name")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email", "message")
