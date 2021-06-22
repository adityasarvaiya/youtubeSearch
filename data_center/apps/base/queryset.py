from safedelete.queryset import SafeDeleteQueryset
from safedelete.models import HARD_DELETE


class SoftDeleteQueryset(SafeDeleteQueryset):
    """
    In case someone passes hard-delete as delete method,
        Optimize delete
    """

    def delete(self, force_policy=None):

        if force_policy == HARD_DELETE:
            # Force Django Queryset to execute rather than Safe-delete
            return super(SafeDeleteQueryset, self).delete()    # pylint: disable=bad-super-call

        # Normal execution
        return super().delete()