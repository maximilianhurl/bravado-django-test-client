import json
from typing import Dict

from bravado.http_client import HttpClient
from bravado.http_future import FutureAdapter, HttpFuture
from bravado_core.response import IncomingResponse


class DjangoTestResponseAdapter(IncomingResponse):
    def __init__(self, django_response):
        self.django_response = django_response

    @property
    def status_code(self):
        return self.django_response.status_code

    @property
    def text(self):
        return self.django_response.content

    @property
    def raw_bytes(self):
        return self.django_response.content

    @property
    def reason(self):
        return self.django_response.content

    @property
    def headers(self):
        # convert django test response headers into a dict
        headers = dict((v[0], v[1]) for _, v in self.django_response._headers.items())

        # bravdo needs content type to be lower case to trigger validation
        headers["content-type"] = headers.get("Content-Type", None)
        return headers

    def json(self, **kwargs):
        return self.django_response.json()

    @property
    def data(self):
        return self.json()


class DjangoTestFutureAdapter(FutureAdapter):
    def __init__(self, client, request) -> None:
        self.client = client
        self.request = request

    def result(self, timeout):
        request = self.request
        request_method = getattr(self.client, request["method"].lower())
        url = request["url"]
        headers = request["headers"]

        # convert data from a string to json
        data = request.get("data", None)
        if data:
            data = json.loads(data)

        # handle get params
        params = request.get('params', {})

        # handle DRF and vanila Django seperately
        if self.client.__class__.__name__ == 'Client':
            response = request_method(url, data or params, **headers, content_type="application/json")
        else:
            response = request_method(url, data or params, **headers, format='json')

        return response


class DjangoTestHttpClient(HttpClient):
    def __init__(self, test_client, *args, **kwargs) -> None:
        self.test_client = test_client
        super().__init__(*args, **kwargs)

    def sanitize_params(self, request_params: Dict):
        sanitized_params = request_params.copy()

        if "connect_timeout" in sanitized_params:
            sanitized_params.pop("connect_timeout")

        if "timeout" in sanitized_params:
            sanitized_params.pop("timeout")

        return sanitized_params

    def request(self, request_params, operation=None, request_config=None):
        sanitized_params = self.sanitize_params(request_params)

        django_test_future = DjangoTestFutureAdapter(self.test_client, sanitized_params)

        return HttpFuture(django_test_future, DjangoTestResponseAdapter, operation, request_config)
