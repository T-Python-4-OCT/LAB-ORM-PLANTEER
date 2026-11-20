
from django.contrib import admin
from .models import Plant, PlantImage, Comment


class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_edible",
        "created_by",
        "created_at",
    )

    list_filter = (
        "category",
        "is_edible",
        "created_at",
    )

    search_fields = (
        "name",
        "about",
    )

    inlines = [PlantImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plant",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = (
        "user__username",
        "plant__name",
        "content",
    )
