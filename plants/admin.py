from django.contrib import admin
from .models import Plant, Comment
admin.site.register([Plant, Comment])
