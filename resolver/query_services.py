from resolver.servicerouter.service_discovery import ServiceDiscovery
from resolver.tagparser.tagparser import Parser

class QueryEngine:
    def __init__(self, registry_endpoint):
        self.registry_endpoint = registry_endpoint
        self.update_network()

    def update_network(self) -> bool:  # This will be triggered regularly via a chron job
        discovery = ServiceDiscovery(self.registry_endpoint)
        self.services = discovery.fetch_services()
        self.clients = discovery.generate_clients(self.services)
        return True
    
    def formulate_data_request(self, role, identifier, term=None):
        if term == None:
            # get request
            pass
        else:
            pass
            # Callback to vocabulary if term exists and if model level or individual level
            # filter service type "data provider" and result of callback
            # 
        # filter potential providers



    def request_recommendation():
        pass

    def parse_tag(self, tag):
        parser = Parser()
        tag = parser.parse_tag(tag)


class Callback:
    def __init__(self):
        pass



# Parse Tag and extract information
# Get role of requester and recommendation of information
# filter out possible services
# Formulate information request