from collections import OrderedDict

from drf_yasg.inspectors import PaginatorInspector
from drf_yasg import openapi


class LimitOffsetPaginatorInspectorClass(PaginatorInspector):

    def get_paginated_response(self, paginator, response_schema):
        """
        :param BasePagination paginator: the paginator
        :param openapi.Schema response_schema: the response schema that must be paged.
        :rtype: openapi.Schema
        """

        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('count', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('next', openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=OrderedDict((
                        ('offset', openapi.Schema(type=openapi.TYPE_INTEGER)),
                        ('limit', openapi.Schema(type=openapi.TYPE_INTEGER))
                    ))
                )),
                ('results', response_schema),
            )),
            required=['results']
        )

    def get_paginator_parameters(self, paginator):
        """
        Get the pagination parameters for a single paginator **instance**.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `paginator`.

        :param BasePagination paginator: the paginator
        :rtype: list[openapi.Parameter]
        """

        return [
            openapi.Parameter('offset', openapi.IN_QUERY, "Offset for Pagination", False, None, openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, "Page Size", False, None, openapi.TYPE_INTEGER)
        ]