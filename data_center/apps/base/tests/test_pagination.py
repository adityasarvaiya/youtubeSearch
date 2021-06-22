from collections import OrderedDict
from unittest import mock

from django.test import SimpleTestCase, tag
from rest_framework.response import Response

from apps.base import pagination


class ViewTest:
    page_default_limit = 20
    view_schema = 'abc'

    def get_view_schema(self):
        pass


@tag('CustomLimitOffsetPagination')
class TestCustomLimitOffsetPagination(SimpleTestCase):
    """TestCases for CustomLimitOffsetPagination class"""

    file_path = 'apps.base.pagination'

    def setUp(self):
        self.lop = pagination.CustomLimitOffsetPagination()

    def test_get_next_offset_both_0(self):
        self.lop.offset = 0
        self.lop.limit = 0
        self.lop.count = 0

        self.assertEqual(
            self.lop.get_next_offset(),
            {'offset': None, 'limit': 0}
        )

    def test_get_next_offset_both_greater_than_count(self):
        self.lop.offset = 10
        self.lop.limit = 10
        self.lop.count = 1

        self.assertEqual(
            self.lop.get_next_offset(),
            {'offset': None, 'limit': 10}
        )

    def test_get_next_offset_lesser(self):
        self.lop.offset = 20
        self.lop.limit = 10
        self.lop.count = 40

        self.assertEqual(
            self.lop.get_next_offset(),
            {'offset': 30, 'limit': 10}
        )

    def test_get_next_offset_equals(self):
        self.lop.offset = 30
        self.lop.limit = 10
        self.lop.count = 40

        self.assertEqual(
            self.lop.get_next_offset(),
            {'offset': None, 'limit': 10}
        )

    def test_get_next_offset_crosses(self):
        self.lop.offset = 31
        self.lop.limit = 10
        self.lop.count = 40

        self.assertEqual(
            self.lop.get_next_offset(),
            {'offset': None, 'limit': 10}
        )

    @mock.patch(f"{file_path}.CustomLimitOffsetPagination.get_next_offset")
    def test_get_paginated_response__normal(self, mock_get_next_offset):
        mock_get_next_offset.return_value = {}
        self.lop.count = 40
        self.lop.schema = 'Test'

        self.assertEqual(
            self.lop.get_paginated_response({}).data,
            Response(OrderedDict([
                ('count', 40),
                ('next', {}),
                ('results', {}),
                ('schema', 'Test')
            ])).data
        )

    @mock.patch(f"{file_path}.CustomLimitOffsetPagination.get_next_offset")
    def test_get_paginated_response__no_schema(self, mock_get_next_offset):
        mock_get_next_offset.return_value = {}
        self.lop.count = 40

        self.assertEqual(
            self.lop.get_paginated_response({}).data,
            Response(OrderedDict([
                ('count', 40),
                ('next', {}),
                ('results', {}),
            ])).data
        )

    def test_paginate_queryset(self):
        view = ViewTest()
        request = mock.MagicMock()

        self.assertEqual(self.lop.paginate_queryset(queryset={}, request=request, view=view), [])

    def test_paginate_queryset__view_schema(self):
        class TestViewWithSchema:
            view_schema = 'a'

        request = mock.MagicMock()

        self.assertEqual(self.lop.paginate_queryset(queryset={}, request=request, view=TestViewWithSchema()), [])

    def test_paginate_queryset__no_view(self):
        request = mock.MagicMock()

        self.assertEqual(self.lop.paginate_queryset(queryset={}, request=request, view=''), [])

    def test_paginate_queryset__view_with_no_attribute(self):
        class TestViewEmpty:
            pass

        request = mock.MagicMock()

        self.assertEqual(self.lop.paginate_queryset(queryset={}, request=request, view=TestViewEmpty()), [])