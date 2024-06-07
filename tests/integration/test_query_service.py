import pytest
import json
from unittest.mock import patch, MagicMock
from resolver.servicerouter.service_discovery import ServiceDiscovery, ServiceAPI
from resolver.query_services import QueryEngine

@pytest.fixture
def mock_services():
    mock_response_file = './resolver/data/registry.json'
    with open(mock_response_file, 'r') as file:
        return json.load(file)

@pytest.fixture
def mock_clients():
    return [MagicMock(), MagicMock()]

def test_query_engine_init(mock_services, mock_clients):
    with patch.object(ServiceDiscovery, 'fetch_services', return_value=mock_services), \
         patch.object(ServiceDiscovery, 'generate_clients', return_value=mock_clients):
        
        registry_endpoint = "http://registry.com"
        query_engine = QueryEngine(registry_endpoint)
        
        assert query_engine.registry_endpoint == registry_endpoint
        assert len(query_engine.services) == len(mock_services)
        assert len(query_engine.clients) == len(mock_clients)

def test_update_network(mock_services, mock_clients):
    with patch.object(ServiceDiscovery, 'fetch_services', return_value=mock_services), \
         patch.object(ServiceDiscovery, 'generate_clients', return_value=mock_clients):
        
        registry_endpoint = "http://registry.com"
        query_engine = QueryEngine(registry_endpoint)
        
        result = query_engine.update_network()
        
        assert result is True
        assert len(query_engine.services) == len(mock_services)
        assert len(query_engine.clients) == len(mock_clients)
