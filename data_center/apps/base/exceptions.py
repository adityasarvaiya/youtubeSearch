from rest_framework import status
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class BadRequest(APIException):
    """
    Our validation error
    """
    status_code = status.HTTP_400_BAD_REQUEST