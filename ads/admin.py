from django.contrib import admin
from .models import Ad

@admin.register(Ad)
class AdModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_public')