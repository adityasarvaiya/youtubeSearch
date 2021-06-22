from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Over-written to define our own format of next and previous
    """

    schema = []

    def paginate_queryset(self, queryset, request, view=None):

        if view:

            if hasattr(view, 'page_default_limit'):
                self.default_limit = view.page_default_limit

            if hasattr(view, 'get_view_schema'):
                self.schema = view.get_view_schema()
            elif hasattr(view, 'view_schema'):
                self.schema = view.view_schema

        return super().paginate_queryset(queryset, request, view)


    def get_next_offset(self):
        """
        Instead of link, we need to provide dict containing offset
        """

        offset = self.offset + self.limit

        if offset >= self.count:
            offset = None

        return {
            "offset": offset,
            "limit": self.limit
        }

    def get_paginated_response(self, data):
        response = OrderedDict([
            ('count', self.count),
            ('next', self.get_next_offset()),
            ('results', data)
        ])

        if self.schema:
            response['schema'] = self.schema

        return Response(response)