from django.test import TestCase, tag

from apps.base.exception_handler import custom_exception_handler


@tag("ExceptionHandler")
class TestExceptionHandler(TestCase):

    def test_custom_exception_handler__normal(self):
        self.assertEqual(custom_exception_handler('l', 'l'), None)