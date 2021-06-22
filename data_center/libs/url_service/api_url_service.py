import logging
import traceback
import json

import requests
from rest_framework import status

from . import namespaces


logger = logging.getLogger(__name__)


class APIURLException(Exception):
    """
    Custom exception when handling URLs
    """



class APIURLService:
    """
    Class to manage micro-service URLs
    """

    def create_url_string(self, url: str, path_params: dict) -> str:
        """
        Fill in Path params in URL and return URL string
        """

        return url.format_map(path_params)

    def join_namespace_with_url(self, namespace, url):
        """
        Join namespace and URL taking care of Trailing and leading slashes
        """

        f_namespace = namespace.rstrip("/")
        f_url = url.lstrip("/")
        return f"{f_namespace}/{f_url}"

    def make_request(self, url: str, namespace: str, method: str, **kwargs):
        """Make external request to a URL using python's request module.

        Args:
            url: URL of the request.
            method: method of the request.
            kwargs: (optional) dict containg extra inputs.
                path_params: (optional) Dictionay of path params if any to be replaced in the path.
                params: (optional) Dictionary or bytes to be sent in the query string.
                headers: (optional) Dictionary of HTTP Headers to send.
                data: (optional) Dictionary or list of tuples, bytes, or file-like object to send in the body.
                json: (optional) A JSON serializable Python object to send in the body.
                timeout: (optional) How many seconds to wait for the server to send data.

        Returns:
            requests.models.Response object.
        """

        path_params = kwargs.pop('path_params', {})
        url = self.create_url_string(url, path_params)

        base = namespaces.NAMESPACE_MAPPING.get(namespace)

        if not base:
            raise APIURLException(f"This namespace {namespace} does not have valid host")

        resolved_url = self.join_namespace_with_url(base, url)

        request_log = '{url} :: {method} :: {request}'.format(
            url=resolved_url,
            method=method,
            request=json.dumps(kwargs),
        )
        logger.info(request_log)

        response = requests.request(method, resolved_url, **kwargs)

        # if status.is_success(response.status_code):
        #     response_log = '{code} :: {content} \n#------------------------------------------#\n'.format(
        #         code=response.status_code,
        #         content=response.content.decode('utf-8'),
        #     )
        #     logger.info(response_log)

        # else:
        #     error = traceback.format_exc()
        #     log = '{error}\n{text}\n#------------------------------------------#\n'.format(
        #         error=error,
        #         text=response.text
        #     )
        #     logger.warning(log)

        if not status.is_success(response.status_code):
            error = traceback.format_exc()
            log = '{error}\n{text}\n#------------------------------------------#\n'.format(
                error=error,
                text=response.text
            )
            logger.warning(log)

        return response
