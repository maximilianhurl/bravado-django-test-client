# Bravado Django Test Client

[![Build Status](https://travis-ci.org/maximilianhurl/bravado-django-test-client.svg?branch=master)](https://travis-ci.org/maximilianhurl/bravado-django-test-client)

[Django Test Client](https://docs.djangoproject.com/en/2.1/topics/testing/tools/\#the-test-client) compatible HTTP Client with [Bravado](https://github.com/Yelp/bravado).

This allows your Django API and OpenAPI v2 (Swagger) specification files to be tested against each other in your unit tests. The aim being to quickly highlight any potential discrepancies between the specification and your actual API.

## Basic Usage

```python
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file
from bravado_django_test_client.django_test_client import DjangoTestHttpClient
from bravado_django_test_client.config import config
from rest_framework.test import APIClient


swagger_file = load_file("schema.yaml")

test_client = APIClient()  # or the standard django test client

bravado_http_client = DjangoTestHttpClient(test_client)

client = SwaggerClient.from_spec(swagger_file, http_client=bravado_http_client, config=config)

# now use as you would a normal bravado client
pet_result = client.pet.getPetById(petId=42).response().result

# any request or response that doesnt match your schema will raise an exception
```

See the [tests directory](https://github.com/maximilianhurl/bravado-django-test-client/blob/master/tests/tests.py) for a more complete example.
