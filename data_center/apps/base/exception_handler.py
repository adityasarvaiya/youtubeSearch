from rest_framework import exceptions, status, views


def custom_exception_handler(exc, context):
    """
    Custom exception handler that changes the drf's default 403 response code
    to 401 for AuthenticationFailed and NotAuthenticated exceptions
    """

    response = views.exception_handler(exc, context)

    if isinstance(exc, (exceptions.AuthenticationFailed, exceptions.NotAuthenticated)):
        response.status_code = status.HTTP_401_UNAUTHORIZED

    return response