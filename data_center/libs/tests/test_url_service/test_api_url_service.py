from unittest import mock

from django.conf import settings
from django.test import SimpleTestCase, tag
from rest_framework import status

from libs.url_service.api_url_service import APIURLService, APIURLException, namespaces


@tag('APIURLService')
class TestAPIURLService(SimpleTestCase):
    """TestCases for api url service class"""

    file_path = 'libs.url_service.api_url_service'

    def test_create_url_string__empty_params(self):
        self.assertEqual(
            APIURLService().create_url_string(url="abc/def", path_params={}),
            "abc/def"
        )

    def test_create_url_string__success(self):
        self.assertEqual(
            APIURLService().create_url_string(url="abc/def/{xyz}", path_params={"xyz": "lmn"}),
            "abc/def/lmn"
        )

    @mock.patch(f"{file_path}.APIURLService.create_url_string")
    def test_make_request__invalid_namespace(self, mock_create_url):
        mock_create_url.return_value = "/abc/xyz"

        with self.assertRaisesMessage(APIURLException, "This namespace abc does not have valid host"):
            APIURLService().make_request("url", "abc", "GET")

    @mock.patch(f"{file_path}.requests.request")
    @mock.patch(f"{file_path}.APIURLService.create_url_string")
    @mock.patch(f"{file_path}.APIURLService.join_namespace_with_url")
    def test_make_request__failed(self, mock_resolved_namespace, mock_create_url, mock_request):
        mock_create_url.return_value = "/abc/xyz"
        mock_resolved_namespace.return_value = "foo.com/abc/xyz"


        response = mock.MagicMock()
        response.status_code = status.HTTP_400_BAD_REQUEST
        mock_request.return_value = response
        self.assertEqual(
            APIURLService().make_request("url", namespaces.TEST_NAMESPACE, "GET", path_params={}),
            response
        )
        mock_request.assert_called_with('GET', "foo.com/abc/xyz")
        mock_resolved_namespace.assert_called_with("test.com", "/abc/xyz")

    @mock.patch(f"{file_path}.requests.request")
    @mock.patch(f"{file_path}.APIURLService.create_url_string")
    def test_make_request__success(self, mock_create_url, mock_request):
        mock_create_url.return_value = "/abc/xyz"

        response = mock.MagicMock()
        response.status_code = status.HTTP_200_OK
        mock_request.return_value = response
        self.assertEqual(
            APIURLService().make_request("url", namespaces.TEST_NAMESPACE, "GET"),
            response
        )

    def test_join_namespace_with_url_trailing_slash(self):
        self.assertEqual(
            APIURLService().join_namespace_with_url(namespace="xyz.com/", url="abc"),
            "xyz.com/abc"
        )

    def test_join_namespace_with_url_trailing_and_leading_slash(self):
        self.assertEqual(
            APIURLService().join_namespace_with_url(namespace="xyz.com/", url="/abc"),
            "xyz.com/abc"
        )

    def test_join_namespace_with_url_with_leading_slash(self):
        self.assertEqual(
            APIURLService().join_namespace_with_url(namespace="xyz.com", url="/abc"),
            "xyz.com/abc"
        )
    def test_join_namespace_with_url_without_trailing_and_leading_slash(self):
        self.assertEqual(
            APIURLService().join_namespace_with_url(namespace="xyz.com", url="abc"),
            "xyz.com/abc"
        )