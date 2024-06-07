import json
import requests
from typing import List, Optional, Union
from pydantic import BaseModel


class Endpoint:
    """
    Represents an API endpoint with its path, method, tags, request body schema, and query parameters.
    """

    def __init__(self, path: str, method: str, tags: List[str], request_body: dict = None, query_params: list = None):
        self.path = path
        self.method = method
        self.request_body = request_body
        self.query_params = query_params
        self.tags = tags


class EndpointFilterCriteria(BaseModel):
    """
    Defines the criteria for filtering API endpoints.
    """
    path: Optional[Union[str, List[str]]] = None
    method: Optional[Union[str, List[str]]] = None
    tags: Optional[Union[str, List[str]]] = None


class APIClient:
    """
    Client for interacting with an API based on its OpenAPI schema.
    Parses the OpenAPI schema to extract endpoint information and provides methods
    to make requests and filter endpoints based on criteria.
    """

    def __init__(self, openapi_schema: dict, client_id: int = None):
        self.client_id = client_id
        self.openapi_version = openapi_schema.get("openapi", {})
        self.openapi_schema = openapi_schema
        self.endpoints = self.parse_openapi_schema(openapi_schema)

    def resolve_ref(self, ref: str) -> dict:
        """
        Resolve $ref to the actual schema definition.

        Args:
            ref (str): The reference string to resolve.

        Returns:
            dict: The resolved schema.
        """
        try:
            ref_path = ref.split('/')[1:]  # Split and remove the initial '#'
            schema = self.openapi_schema
            for part in ref_path:
                schema = schema[part]
            return schema
        except KeyError:
            raise ValueError(f"Invalid reference: {ref}")

    def parse_openapi_schema(self, openapi_schema: dict) -> List[Endpoint]:
        """
        Parse the OpenAPI schema to extract endpoint information.

        Args:
            openapi_schema (dict): The OpenAPI schema.

        Returns:
            List[Endpoint]: A list of Endpoint objects.
        """
        endpoints = []
        paths = openapi_schema.get("paths", {})

        for path, methods in paths.items():
            for method, details in methods.items():
                request_body_schema = details.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")

                if request_body_schema and "$ref" in request_body_schema:
                    request_body_schema = self.resolve_ref(request_body_schema["$ref"])

                endpoint = Endpoint(
                    path=path,
                    method=method,
                    tags=details.get("tags", []),
                    request_body=request_body_schema,
                    query_params=details.get("parameters")
                )

                endpoints.append(endpoint)
        return endpoints

    def make_request(self, root_url: str, endpoint: Endpoint, **kwargs) -> requests.Response:
        """
        Make an HTTP request to an endpoint.

        Args:
            root_url (str): The base URL of the API.
            endpoint (Endpoint): The endpoint to make the request to.
            **kwargs: Additional arguments for the request.

        Returns:
            requests.Response: The HTTP response.
        """
        try:
            url = root_url + endpoint.path
            method = endpoint.method.lower()
            if method == "get":
                response = requests.get(url, params=kwargs)
            elif method == "post":
                response = requests.post(url, json=kwargs.get("data"))
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response
        except requests.RequestException as e:
            raise SystemError(f"Request to {url} failed: {e}")

    def filter_endpoints(self, criteria: EndpointFilterCriteria) -> List[Endpoint]:
        """
        Filter the endpoints based on the given criteria.

        Args:
            criteria (EndpointFilterCriteria): The criteria to filter the endpoints.

        Returns:
            List[Endpoint]: A list of endpoints that match the criteria.
        """
        filtered_endpoints = self.endpoints
        criteria_dict = criteria.model_dump(exclude_unset=True)

        for key, value in criteria_dict.items():
            if isinstance(value, list):
                new_filtered_endpoints = []
                for endpoint in filtered_endpoints:
                    for filter_val in value:
                        if filter_val in getattr(endpoint, key):
                            new_filtered_endpoints.append(endpoint)
                            break  # Avoid adding the same endpoint multiple times
                filtered_endpoints = new_filtered_endpoints
            else:
                filtered_endpoints = [
                    endpoint for endpoint in filtered_endpoints
                    if value in getattr(endpoint, key)
                ]

        return filtered_endpoints
    