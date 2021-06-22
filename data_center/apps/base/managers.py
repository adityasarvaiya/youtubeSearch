from safedelete import managers as safedelete_managers

from apps.base.queryset import SoftDeleteQueryset


class SoftDeleteManager(safedelete_managers.SafeDeleteManager):
    """
    Default Manager for Soft-Delete class
    Over-ridden to use our queryset, rather than default
    """

    _queryset_class = SoftDeleteQueryset


class SoftDeleteAllManager(SoftDeleteManager, safedelete_managers.SafeDeleteAllManager):
    """
    To Manage "all_objects"
    """
