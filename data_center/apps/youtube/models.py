from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel
from apps.youtube.managers import BulkManager, BulkAllManager


class Videos(BaseModel):
    """
    Model to store details of Youtube videos
    """

    video_id = models.CharField(
    	primary_key=True,
    	max_length=255,
        help_text=_("unique id.")
    )
    published_at = models.DateTimeField(
        help_text=_("The date and time that the video was published. Note that"
        	"this time might be different than the time that the video was uploaded.")
    )
    title = models.CharField(
    	max_length=500,
        help_text=_("stores the video's title.")
    )
    description = models.CharField(
    	max_length=5000,
    	null=True,
        blank=True,
        help_text=_("stores the video's description.")
    )
    thumbnails_info = JSONField(
        help_text=_("A map of thumbnail images associated with the video."
        	"For each object in the map, the key is the name of the thumbnail"
        	"image, and the value is an object that contains other information"
        	"about the thumbnail.")
    )
    channel_id = models.CharField(
    	max_length=100,
        help_text=_("The ID that YouTube uses to uniquely identify the "
        	"channel that the video was uploaded to.")
    )
    channel_title = models.CharField(
    	max_length=200,
        help_text=_("Channel title for the channel that the video belongs to.")
    )

    objects = BulkManager()
    all_objects = BulkAllManager()

    class Meta:
        ordering = ['-published_at']
