import logging

import pytest
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file
from bravado_django_test_client.django_test_client import DjangoTestHttpClient
from bravado_django_test_client.config import config
from django.test import Client
from jsonschema.exceptions import ValidationError
from rest_framework.test import APIClient
from swagger_spec_validator import SwaggerValidationError


@pytest.fixture(scope="session")
def swagger_file():
    swagger_file = load_file("swagger.yaml")
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


def test_params(swagger_client_django_client):
    response = swagger_client_django_client.tests.GetParamsTest(paramInt=1).response()
    assert response.incoming_response.status_code == 200
    assert response.result["paramInt"] == 1
    assert response.result["paramString"] is None
    bytes_response = b'{"paramInt": 1, "paramString": null}'
    assert response.incoming_response.text == bytes_response
    assert response.incoming_response.raw_bytes == bytes_response
    assert response.incoming_response.reason == bytes_response

    response = swagger_client_django_client.tests.GetParamsTest(paramInt=1, paramString="test").response()
    assert response.incoming_response.status_code == 200
    assert response.result["paramInt"] == 1
    assert response.result["paramString"] == "test"


cat_to_create = {
    "id": "1",
    "name": "Tar tar sauce",
    "color": "Brown",
    "age": 1,
    "friends": [],
}


def test_cat_create(swagger_client_django_client):
    response = swagger_client_django_client.cats.createCat(cat=cat_to_create).response()
    assert response.incoming_response.status_code == 201
    assert response.result["id"] == "1"
    assert response.result["name"] == "Tar tar sauce"
    assert response.result["color"] == "Brown"
    assert response.result["age"] == 1
    assert response.result["friends"] == []


def test_cat_create_rest_framework(swagger_client_drf_client):
    response = swagger_client_drf_client.cats.createCat(cat=cat_to_create).response()
    assert response.incoming_response.status_code == 201
    assert response.result["id"] == "1"
    assert response.result["name"] == "Tar tar sauce"
    assert response.result["color"] == "Brown"
    assert response.result["age"] == 1
    assert response.result["friends"] == []
    assert response.incoming_response.data == cat_to_create


def test_cat_list_rest_framework(swagger_client_drf_client):
    request_options = {
        "connect_timeout": 1,
        "timeout": 1,
        "headers": {
            "CAT_HEADER": "meeow",
        }
    }
    result = swagger_client_drf_client.cats.listCats(_request_options=request_options).result()
    assert result["CAT_HEADER"] == request_options["headers"]["CAT_HEADER"]
    assert result["results"][0]["id"] == "1"
    assert result["results"][0]["name"] == "Tar tar sauce"
    assert result["results"][0]["color"] == "Brown"
    assert result["results"][0]["age"] == 1
    assert result["results"][0]["friends"] == []


def test_cat_update_rest_framework(swagger_client_drf_client):
    cat = {
        "id": "4",
        "name": "not minky",
        "color": "Brown",
    }
    response = swagger_client_drf_client.cats.updateCat(cat_name="minky", cat=cat).response()
    assert response.incoming_response.status_code == 200
    assert response.result["id"] == "4"
    assert response.result["name"] == "minky"
    assert response.result["color"] == "Brown"


def test_cat_invalid_request(swagger_client_drf_client):
    cat = {
        "id": "4",
    }

    with pytest.raises(ValidationError, match="'name' is a required property"):
        swagger_client_drf_client.cats.updateCat(cat_name="minky", cat=cat).response()
