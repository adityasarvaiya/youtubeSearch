"""Command for creating super-user."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import os


class Command(BaseCommand):
    """Defines initadmin command that creates admin account"""
    # Todo add individual accounts for each person that needs a super user.

    def handle(self, *args, **options):
        """Create an admin account if no user is present.

        Notes
        -----
        1. Create SuperUser account with admin and staff privileges if no user
        account exist
        2. Write error to stdout if User account already exist
        """
        user = get_user_model()
        if user.objects.count() == 0:
                admin = user.objects.create_superuser(
                    username=os.environ["ADMIN_SUPERUSER_USERNAME"],
                    email=os.environ["ADMIN_SUPERUSER_EMAIL"],
                    password=os.environ["ADMIN_SUPERUSER_PASSWORD"],
                )

                self.stdout.write(
                    self.style.SUCCESS('Admin account created! :)'))
        else:
            error = 'Admin accounts can only be initialized ' \
                    'if no Accounts exist'
            self.stdout.write(self.style.ERROR('Error:- ' + str(error)))