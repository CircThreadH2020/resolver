import json
import pytest
import requests
from requests.models import Response
from unittest.mock import patch
from pydantic import BaseModel
from resolver.servicerouter.client_generator import APIClient, Endpoint, EndpointFilterCriteria


# Load OpenAPI schema from an external JSON file
def load_openapi_schema(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)


# Load the schema (assuming the file is in the same directory as this script)
mock_openapi_schema = load_openapi_schema('resolver/data/openapi.json')


def test_resolve_ref():
    client = APIClient(mock_openapi_schema)
    resolved_schema = client.resolve_ref("#/components/schemas/TestSchema")
    assert resolved_schema == {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "value": {"type": "integer"}
        }
    }


def test_parse_openapi_schema():
    client = APIClient(mock_openapi_schema)
    endpoints = client.parse_openapi_schema(mock_openapi_schema)
    assert len(endpoints) == 2
    assert endpoints[0].path == "/example"
    assert endpoints[0].method == "get"
    assert endpoints[1].path == "/test"
    assert endpoints[1].method == "post"


def test_filter_endpoints():
    client = APIClient(mock_openapi_schema)
    criteria = EndpointFilterCriteria(tags="example-tag")
    filtered_endpoints = client.filter_endpoints(criteria)
    assert len(filtered_endpoints) == 1
    assert filtered_endpoints[0].path == "/example"

