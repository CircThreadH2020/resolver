import json


class crawler():
    def __init__(self):
        self.addresses = self.__load_service_addresses()

# Change private methods in the future to external utils function files
    def __load_service_addresses(self):
        #file = open("data/serviceapis.json", "r")
        file = open("DOM_resolver/data/serviceapis.json", "r")
        addresses = {}
        apis = json.load(file)
        for services in apis:
            addresses[services] = apis[services]["ROOT_ADDRESS"] + apis[services]["ALL_METADATA"]
        return addresses


    def retrieve_metadata(self):
        import requests
        metadata = {}
        for key in self.addresses:
            response = requests.get(self.addresses[key])
            items = self.__parse_response(response)
            metadata[key] = items
        return metadata


    def __parse_response(self, response):
        response = response.json()
        response = response["metadata"]
        items =  []
        for i in response:
            items.append(i["metaData"])
        return items
    

    def save_metadata_list(self, metadata):
        with open("DOM_resolver/data/metadatalist.json", "w") as fp:
            json.dump(metadata, fp)


if __name__ == "__main__":
    c = crawler()
    re = c.retrieve_metadata()
    c.save_metadata_list(re)
