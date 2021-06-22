from psqlextra.manager import PostgresManager, PostgresQuerySet

from apps.base.managers import SoftDeleteManager, SoftDeleteAllManager
from apps.base.queryset import SoftDeleteQueryset


class QuerySet(SoftDeleteQueryset, PostgresQuerySet):
	"""Combines the functionality of bulk update and sofedelete"""


class BulkManager(SoftDeleteManager, PostgresManager):
    """
    Provides psqlextra functionality, softdelete functionality and
    bulk update functionality
    """

    _queryset_class = QuerySet


class BulkAllManager(BulkManager, SoftDeleteAllManager):
    """
    Provides psqlextra functionality, softdelete functionality and
    bulk update functionality on all objects
    """
