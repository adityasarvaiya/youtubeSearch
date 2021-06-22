from unittest import mock

from django.test import TestCase, tag
from kombu.exceptions import KombuError

from apps.base.publisher import publish


@tag("Publisher")
class TestPublisher(TestCase):
    """ Test cases for publisher """

    file_path = 'apps.base.publisher'

    @mock.patch(f'{file_path}.APP_NAMESPACE')
    def test_publish__normal(self, mock_app_namespace):
        self.assertEqual(publish(['abc'], 'p360'), None)

    @mock.patch(f'{file_path}.APP_NAMESPACE')
    def test_publish__exchanges_not_list(self, mock_app_namespace):
        self.assertEqual(publish('', 'test'), None)

    def test_publish__empty_exchange_app(self):
        self.assertEqual(publish(['abc'], 'test'), None)

    @mock.patch(f'{file_path}.APP_NAMESPACE')
    def test_publish__kombu_error(self, mock_app_namespace):
        mock_app_namespace.get().send_task.side_effect = KombuError

        self.assertEqual(publish(['abc'], ''), None)