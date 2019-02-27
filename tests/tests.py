import logging

import pytest
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file
from bravado_django_test_client.django_test_client import DjangoTestHttpClient
from bravado_django_test_client.config import config
from django.test import Client
from rest_framework.test import APIClient
from swagger_spec_validator import SwaggerValidationError


# add test for DRF api client
# add test for request validation failure
# add test for response data validation
# add test for POST and json
# add tests for DELETE
# add test for PUT
# add test for nested objects

@pytest.fixture(scope="session")
def swagger_file():
    swagger_file = load_file('swagger.yaml')
    return swagger_file


@pytest.fixture()
def swagger_client_django_client(swagger_file, caplog):
    caplog.set_level(logging.WARNING)
    try:
        client = SwaggerClient.from_spec(swagger_file, http_client=DjangoTestHttpClient(Client()), config=config)
    except SwaggerValidationError:
        raise Exception("Invalid swagger schema - check against https://editor.swagger.io/")
    return client


@pytest.fixture()
def swagger_client_drf_client(swagger_file, caplog):
    caplog.set_level(logging.WARNING)
    try:
        client = SwaggerClient.from_spec(swagger_file, http_client=DjangoTestHttpClient(APIClient()), config=config)
    except SwaggerValidationError:
        raise Exception("Invalid swagger schema - check against https://editor.swagger.io/")
    return client


def test_answer(swagger_client_django_client):
    response = swagger_client_django_client.tests.GetParamsTest(paramInt=1).response()
    assert response.incoming_response.status_code == 200
    assert response.result["paramInt"] == 1
    assert response.result["paramString"] is None
    bytes_response = b'{"paramInt": 1, "paramString": null}'
    assert response.incoming_response.text == bytes_response
    assert response.incoming_response.raw_bytes == bytes_response
    assert response.incoming_response.reason == bytes_response

    response = swagger_client_django_client.tests.GetParamsTest(paramInt=1, paramString='test').response()
    assert response.incoming_response.status_code == 200
    assert response.result["paramInt"] == 1
    assert response.result["paramString"] == 'test'
