from rest_framework import serializers

from apps.youtube.models import Videos


class VideosModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Videos
		fields = ('video_id', 'published_at', 'title',
				  'description', 'thumbnails_info', 'channel_id',
			  	  'channel_title')
