from django.contrib import admin
from .models import ServiceLog


@admin.register(ServiceLog)
class ServiceLogAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('created_at', 'service_name', 'level', 'short_message')

    # Filters on the right sidebar
    list_filter = ('level', 'service_name', 'created_at')

    # Search bar at the top
    search_fields = ('service_name', 'message')

    # Make the list read-only (usually you don't want to edit logs)
    readonly_fields = ('service_name', 'level', 'message', 'payload', 'created_at')

    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Log Message"