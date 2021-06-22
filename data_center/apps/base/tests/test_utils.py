from unittest import mock

from django.test import TestCase, tag
from jwt.exceptions import ExpiredSignatureError
from rest_framework import status

from apps.base import constants as base_constants
from apps.base.utils import validate_jwt_token,\
    ConstantEnum, issue_jwt_token


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestClass(ConstantEnum):
    PATIENT = 'patient'
    PROFILE = 'profile'


@tag('ConstantEnum')
class TestConstantEnum(TestCase):
    """ Test cases for ConstantEnum class."""
            
    def test_new__normal(self):
        self.assertEqual(TestClass.PATIENT, 'patient')

    def test_get_item(self):
        self.assertEqual(TestClass["PATIENT"], 'patient')

    def test_next_item(self):
        test_iter = iter(TestClass)

        self.assertEqual(next(test_iter), ('patient', 'PATIENT'))
        self.assertEqual(next(test_iter), ('profile', 'PROFILE'))

    def test_next_item__exception(self):
        self.assertRaises(StopIteration, next, TestClass)


@tag('BaseUtils')
class TestUtils(TestCase):
    file_path = 'apps.base.utils'

    def test_validate_jwt_token__invalid_token_error(self):
        self.assertEqual(
            validate_jwt_token('d', 'd'),
            (base_constants.JWT_INVALID, None)
        )

    @mock.patch(f'{file_path}.jwt.decode', side_effect=ExpiredSignatureError)
    def test_validate_jwt_token__expired_signature_error(self, mock_decode):
        self.assertEqual(
            validate_jwt_token('d', 'd'),
            (base_constants.JWT_EXPIRED, None)
        )
        mock_decode.assert_called()

    @mock.patch(f'{file_path}.jwt.encode')
    def test_issue_jwt_token__normal(self, mock_encode):
        class TestJwt:

            @staticmethod
            def decode(option):
                pass

        mock_encode.return_value = TestJwt

        self.assertEqual(
            issue_jwt_token({'token': 'abc'}, 'RS256'), None
        )
        mock_encode.assert_called()