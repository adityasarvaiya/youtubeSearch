from django.contrib import admin

from apps.youtube.models import Videos


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    """
    Admin for Videos Model
    """

    list_display = ['video_id', 'title', 'description', 'thumbnails_info', 'published_at']
    search_fields = ['video_id', 'title', 'description']
