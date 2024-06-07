import pytest
import os
import json
from unittest.mock import patch, mock_open
from pydantic import ValidationError
from resolver.servicerouter.client_generator import APIClient
from resolver.servicerouter.service_discovery import ServiceDiscovery, ServiceAPI, ServiceFilterCriteria  # Adjust import as necessary

@pytest.fixture
def mock_services():
    mock_response_file = './resolver/data/registry.json'
    with open(mock_response_file, 'r') as file:
        return json.load(file)

@pytest.fixture
def service_discovery():
    return ServiceDiscovery()

def test_fetch_services_from_registry(service_discovery, mock_services):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_services
        mock_get.return_value.raise_for_status = lambda: None
        
        services = service_discovery.fetch_services()
        
        assert len(services) == 2
        assert services[0].serviceName == "Digital Object Memory Resolver"
        assert services[1].serviceName == "CircThread Event interpreation and Information Recommendation Service"

def test_fetch_openapi_schema(service_discovery, mock_services):
    service = ServiceAPI(**mock_services["Digital Object Memory Resolver"], serviceName="Digital Object Memory Resolver")
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"openapi": "3.0.0"}
        mock_get.return_value.raise_for_status = lambda: None
        
        schema = service_discovery.fetch_openapi_schema(service)
        
        assert schema["openapi"] == "3.0.0"

def test_filter_services(service_discovery, mock_services):
    services = [ServiceAPI(**data, serviceName=name) for name, data in mock_services.items()]
    criteria = ServiceFilterCriteria(serviceTags="test")
    
    filtered_services = service_discovery.filter_services(services, criteria)
    
    assert len(filtered_services) == 1
    assert filtered_services[0].serviceName == "Digital Object Memory Resolver"
