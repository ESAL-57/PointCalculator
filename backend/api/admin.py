from django.contrib import admin

from .models import SearchLog


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ("game_name", "tag_line", "success", "created_at")
    list_filter = ("success", "created_at")
    search_fields = ("game_name", "tag_line", "message")
    readonly_fields = ("game_name", "tag_line", "success", "message", "created_at")
    ordering = ("-created_at",)
