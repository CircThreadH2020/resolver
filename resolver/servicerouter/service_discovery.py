import os
import json
import requests
from typing import List, Optional, Union
from pydantic import BaseModel, ValidationError
from resolver.servicerouter.client_generator import APIClient


class ServiceAPI(BaseModel):
    """
    Represents a service with its metadata and OpenAPI documentation address.
    """
    serviceName: str
    id: int
    rootAddress: str
    apiDocumentationAdress: str
    serviceType: str
    serviceTags: List[str]
    serviceOwner: str
    maintainerContact: str
    maintainanceStatus: str
    sourceCode: str
    version: str
    lastUpdated: str


class ServiceFilterCriteria(BaseModel):
    """
    Defines criteria for filtering services.
    """
    serviceName: Optional[Union[str, List[str]]] = None
    id: Optional[Union[int, List[int]]] = None
    rootAddress: Optional[Union[str, List[str]]] = None
    apiDocumentationAdress: Optional[Union[str, List[str]]] = None
    serviceType: Optional[Union[str, List[str]]] = None
    serviceTags: Optional[Union[str, List[str]]] = None
    serviceOwner: Optional[Union[str, List[str]]] = None
    maintainerContact: Optional[Union[str, List[str]]] = None
    maintainanceStatus: Optional[Union[str, List[str]]] = None
    sourceCode: Optional[Union[str, List[str]]] = None
    version: Optional[Union[str, List[str]]] = None
    lastUpdated: Optional[Union[str, List[str]]] = None


class ServiceDiscovery:
    """
    Handles service discovery, fetching OpenAPI schemas, and generating API clients.
    """

    def __init__(self, get_all_registered_services_endpoint: str = None):
        self.registry_server = get_all_registered_services_endpoint

    def fetch_services(self) -> List[ServiceAPI]:
        """
        Fetch services from the registry server or a local mock file.

        Returns:
            List[ServiceAPI]: A list of discovered services.
        """
        try:
            response = requests.get(self.registry_server)
            response.raise_for_status()
            services = self.__parse_services(response.json())
            if self.__save_discovered_services(services):
                return services
        except requests.RequestException as e:
            print(f"Error fetching service endpoints from registry: {e}")
            raise e

    def __parse_services(self, response: dict) -> List[ServiceAPI]:
        """
        Parse the registry response to create a list of ServiceAPI instances.

        Args:
            response (dict): The registry response containing service information.

        Returns:
            List[ServiceAPI]: A list of ServiceAPI instances.
        """
        services = []
        for service_name, service_info in response.items():
            try:
                service_info['id'] = int(service_info['id'])
                service_api = ServiceAPI(**service_info, serviceName=service_name)
                services.append(service_api)
            except (ValidationError, ValueError) as e:
                print(f"Error parsing service {service_name}: {e}")
        return services

    def __save_discovered_services(self, services: List[ServiceAPI]) -> bool:
        """
        Save discovered services' metadata to JSON files.

        Args:
            services (List[ServiceAPI]): The list of services to save.

        Returns:
            bool: True if services were saved successfully, False otherwise.
        """
        try:
            for service_instance in services:
                service_name = service_instance.serviceName.replace(" ", "_")
                output_dir = os.path.abspath(f'./resolver/data/discovery/services/{service_name}')
                os.makedirs(output_dir, exist_ok=True)

                file_name = os.path.join(output_dir, "info.json")
                with open(file_name, "w") as file:
                    json.dump(service_instance.model_dump(), file)
            return True
        except (OSError, IOError) as e:
            print(f"Error saving discovered services: {e}")
            raise e

    def fetch_openapi_schema(self, service: ServiceAPI) -> dict:
        """
        Fetch the OpenAPI schema for a given service.

        Args:
            service (ServiceAPI): The service for which to fetch the OpenAPI schema.

        Returns:
            Optional[dict]: The OpenAPI schema, or None if fetching failed.
        """
        try:
            response = requests.get(service.apiDocumentationAdress)
            response.raise_for_status()
            openapi_schema = response.json()
            if self.__save_openapi_schema(openapi_schema, service.serviceName):
                return openapi_schema
        except requests.RequestException as e:
            print(f"Error fetching OpenAPI schema from {service.apiDocumentationAdress}: {e}")
            raise e

    def __save_openapi_schema(self, openapi_schema: dict, service_name: str) -> bool:
        """
        Save the OpenAPI schema to a JSON file.

        Args:
            openapi_schema (dict): The OpenAPI schema to save.
            service_name (str): The name of the service.

        Returns:
            bool: True if the schema was saved successfully, False otherwise.
        """
        try:
            service_name = service_name.replace(" ", "_")
            output_dir = os.path.abspath(f'./resolver/data/discovery/services/{service_name}')
            os.makedirs(output_dir, exist_ok=True)

            schema_file = os.path.join(output_dir, "openapi.json")
            with open(schema_file, "w") as f:
                json.dump(openapi_schema, f)
            return True
        except (OSError, IOError) as e:
            print(f"Error saving OpenAPI schema: {e}")
            raise e

    def filter_services(self, services: List[ServiceAPI], criteria: ServiceFilterCriteria) -> List[ServiceAPI]:
        """
        Filter services based on given criteria.

        Args:
            services (List[ServiceAPI]): The list of services to filter.
            criteria (ServiceFilterCriteria): The criteria to use for filtering.

        Returns:
            List[ServiceAPI]: A list of services that match the criteria.
        """
        filtered_services = []
        criteria_dict = criteria.model_dump(exclude_unset=True)

        for key, value in criteria_dict.items():
            if isinstance(value, list):
                for service in services:
                    for filter_val in value:
                        if filter_val in getattr(service, key):
                            filtered_services.append(service)
                            break
            else:
                for service in services:
                    if value in getattr(service, key):
                        filtered_services.append(service)

        return filtered_services

    def generate_clients(self, services:List[ServiceAPI]) -> List[APIClient]:
        """
        Generate API clients from the OpenAPI schemas of the given services.

        Args:
            services (List[ServiceAPI]): The list of services to generate clients for.

        Returns:
            List[APIClient]: A list of generated API clients.
        """
        clients = []
        for service in services: 
            try:
                clients.append(APIClient(self.fetch_openapi_schema(service)))
            except Exception as e:
                print(f"Error generating API client: {e}")
                raise e
        return clients
