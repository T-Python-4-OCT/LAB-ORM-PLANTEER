from django.contrib import admin
from .models import Contact, MainComment


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'email',
        'created_at',
    )

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'message',
    )

    list_filter = ('created_at',)

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)

admin.site.register(MainComment)