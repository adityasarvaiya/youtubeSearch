import logging

from constance import config as live_settings
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from djangorestframework_camel_case.util import underscoreize
from psqlextra.query import ConflictAction
from rest_framework import status


from apps.base.exceptions import ServiceUnavailable
from apps.youtube.models import Videos
from apps.youtube.serializers import VideosModelSerializer
from apps.youtube import constants as youtube_constants
from libs.url_service import api_url_service, url_constants, namespaces

logger = logging.getLogger(__name__)


def convert_datatime_to_rfc_3339_format(date):
    """ Will remove offset and append `z` to the datetime object """
    return date.replace(tzinfo=None).isoformat()+'Z'


class YouTube:
    """ Used to fetch and save the youtube videos """

    def __init__(self):
        self.search_query = live_settings.SEARCH_QUERY
        self.serializer = VideosModelSerializer
        self.model = Videos

    def get_api_key(self):
        return settings.YOUTUBE_API_KEY

    def get_latest_datatime_from_db(self):
        latest_video_obj = Videos.objects.all().order_by('-published_at').first()
        return latest_video_obj.published_at if latest_video_obj else None

    def get_cached_latest_sync_datetime(self):
        return cache.get(key=youtube_constants.CACHE_KEY_YOUTUBE_LATEST_SYNC_DATETIME, default='')

    def add_latest_sync_datetime_to_cache(self, latest_datatime):
        cache.set(
            key=youtube_constants.CACHE_KEY_YOUTUBE_LATEST_SYNC_DATETIME,
            value=latest_datatime,
            timeout=None
        )

    def get_latest_datatime(self):
        latest_datatime = self.get_cached_latest_sync_datetime()
        if not latest_datatime:
            # DB datetime object format is not supported by youtube directly
            # Hence we convert it to RFC 3339 format before using it
            latest_datatime_from_db = self.get_latest_datatime_from_db()
            return (
                convert_datatime_to_rfc_3339_format(
                    latest_datatime_from_db
                ) if latest_datatime_from_db 
                else live_settings.DEFAULT_LATEST_VIDEO_DATETIME
            )
        return latest_datatime

    def fetch_video_details(self, pagetoken):
        query_params = {
            'key': self.get_api_key(),
            'q': self.search_query,
            'publishedAfter': self.get_latest_datatime(),
            'type': 'video',
            'part': 'snippet',
            'order': 'date',
            'maxResults': 50
        }
        if pagetoken:
            query_params['pageToken'] = pagetoken

        response = api_url_service.APIURLService().make_request(
            url=url_constants.SEARCH,
            namespace=namespaces.YOUTUBE_NAMESPACE,
            method='GET',
            params=query_params
        )

        if not status.is_success(response.status_code):
            logger.error('Could not update patient data in patient auth service')
            raise ServiceUnavailable(
                _('Internal Error occured due to, {content}.'
                  'Update the app and try again').format(content=response.content)
            )

        return response

    def preprocess_data(self, data):
        processed_data = []
        next_page_token = data.get('next_page_token')
        items = data.get('items', [])
        latest_datatime = None

        if items:
            # as search response results are sorted in reverse chronological order
            # based on the date they were created. we can take first object as the latest object.
            latest_datatime = items[0]['snippet']['published_at']

        for video_data in items:
            data = video_data['snippet']
            data['video_id'] = video_data['id']['video_id']
            data['thumbnails_info'] = data['thumbnails']

            # We will also remove unwanted data else it will raise an error while doing bulk insert
            data.pop('thumbnails', None)
            data.pop('live_broadcast_content', None)
            data.pop('publish_time', None)
            processed_data.append(data)
        return processed_data, next_page_token, latest_datatime

    def save_responses(self, pagetoken=None, epochs=live_settings.EPOCHS, save_latest_sync_datetime=True):
        response = self.fetch_video_details(pagetoken)
        data, next_page_token, latest_datatime = self.preprocess_data(underscoreize(response.json()))
        self._save(data=data)

        if save_latest_sync_datetime:
            # we will save latest datetime only for the first response
            self.add_latest_sync_datetime_to_cache(latest_datatime)

        # This is used only when we want to fetch response multiple times
        if epochs and next_page_token:
            self.save_responses(
                pagetoken=next_page_token, epochs=epochs-1, save_latest_sync_datetime=False
            )

    def is_valid_data(self, error):
        # If there is no error
        if not error:
            return True

        # serializer will give an error if video id already exists
        # but we want to allow data packet having this error only
        record_id_error = error.get('video_id', [])
        if (
                len(error.keys()) == 1
                and
                len(record_id_error) == 1
                and
                str(record_id_error[0]).endswith('videos with this video id already exists.')
        ):
            return True

        return False

    def save(self, initial_data):
        if not initial_data:
            return

        # Here we used bulk insert to optimize the insertion process
        (
            self.model.objects
            .on_conflict(['video_id'], ConflictAction.UPDATE)
            .bulk_insert(
                initial_data
            )
        )

    def _save(self, data):
        serializer = self.serializer(data=data, many=True)
        serializer.is_valid()

        initial_data = data
        if serializer.errors:
            initial_data = []
            for _data, error in zip(data, serializer.errors):
                if self.is_valid_data(error):
                    initial_data.append(_data)
                else:
                    logger.error(
                        f'Could not process Youtube search response '
                        f'where error is {error} and data is: {_data}'
                    )

        self.save(initial_data)
