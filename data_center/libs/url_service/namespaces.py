''' Constants for base urls for different micro-services we use go here'''
from django.conf import settings

TEST_NAMESPACE = 'test'
YOUTUBE_NAMESPACE = 'youtube'

NAMESPACE_MAPPING = {
	TEST_NAMESPACE: 'test.com',
	YOUTUBE_NAMESPACE: 'https://www.googleapis.com/youtube/v3/'
}
