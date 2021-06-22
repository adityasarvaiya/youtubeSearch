from drf_yasg import openapi
from django.test import TestCase, tag


class ResponseSchema:
    pass


@tag("LimitOffsetPaginatorInspectorClass")
class TestLimitOffsetPaginatorInspectorClass(TestCase):
    """ Test cases for publisher """

    def test_get_paginated_response__normal(self):
        from apps.base.inspectors import LimitOffsetPaginatorInspectorClass

        self.assertEqual(type(LimitOffsetPaginatorInspectorClass(view='d', path='', method='Get',
                                                                 components='f', request='')
                              .get_paginated_response(['abc'], ResponseSchema())), openapi.Schema)

    def test_get_paginator_parameters(self):
        from apps.base.inspectors import LimitOffsetPaginatorInspectorClass

        self.assertEqual(LimitOffsetPaginatorInspectorClass(view='d', path='', method='Get',
                                                            components='f', request='')
                         .get_paginator_parameters(['abc'])[0], openapi.Parameter('offset', openapi.IN_QUERY,
                                                                                  'Offset for Pagination', False, None,
                                                                                  openapi.TYPE_INTEGER))