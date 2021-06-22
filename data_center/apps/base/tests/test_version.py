from django.test import TestCase, tag

import version


@tag('version', 'integration')
class VersionTest(TestCase):

    def test_check_correct_format(self):
        self.assertRegex(version.__version__, r"v\d+.\d+.\d+( RC)?") # pylint: disable=no-member