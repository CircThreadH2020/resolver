import json
import requests

def parse_tag(p_tag):
    # ToDo: reach through exeption handling of functions
    tag = split_p_tag(p_tag)
    tag = map_tag(tag)
    return tag


def split_p_tag(p_tag):
    try:
        tag = p_tag.split("/")
    except ValueError as e:
        return e
    return tag


def map_tag(tag):
    dict_tag = {}
    # distinct between digital link and plain number
    if len(tag) == 1:
        dict_tag["unknown"] = tag[0]
    else:
        for i in range(len(tag)):
            if tag[i] == "01":
                dict_tag['GTIN'] = tag[i+1]
            elif tag[i] == "22":
                dict_tag["consumer product variant"] = tag[i+1]
            elif tag[i] == "10":
                dict_tag["batch number"] = tag[i+1]
            elif tag[i] == "21":
                dict_tag["serial number"] = tag[i+1]
    # A validation of the parsed values must follow in the future
    return dict_tag


def generate_route(tag, term):
    route = {}
    check = check_term_source(term)
    if check != None:
        info = read_out_registry(check)
        if "unknown" in tag:
            route[term] = info["ROOT_ADDRESS"] + info["DATA"] + tag["unknown"]
        else:
            route[term] = info["ROOT_ADDRESS"] + info["DATA"] + tag[info["ID"]]
    for key in route:
        if check_term_availability(term, route[key]) == True:
            return route
        else: # Implement error handling
            return route


def read_out_registry(source):
    #file = open("data/serviceapis.json", "r")
    file = open("DOM_resolver/data/serviceapis.json", "r")
    registry = json.load(file)
    if source in registry:
        serviceInformation = registry[source]
        return serviceInformation
    else:
        raise ValueError("service not registered")
    

def check_term_source(term):
    # in the future change to database with the terms
    #file = open("data/metadatalist.json", "r")
    file = open("DOM_resolver/data/metadatalist.json", "r")
    metadatasources = json.load(file)
    for source in metadatasources:
        for i in metadatasources[source]:
            if term == i:
                return source
    return None


def check_term_availability(term, url):
    response = requests.get(url)
    response = response.json()
    keyword = "metaData"
    allterms = []
    stringified = json.dumps(response)
    for i in range(stringified.count(keyword)):
        stringified = stringified[stringified.find(keyword)+len(keyword)+1:]
        snipet = stringified[stringified.find("\"")+1:stringified.find(",")-1]
        snipet = snipet.strip()
        allterms.append(snipet)
        stringified = stringified[stringified.find(","):]
    if term in allterms:
        return True
    return False


if __name__ == "__main__":
    TAG1 = "18"
    print (TAG1)
    tag = parse_tag(TAG1)
    print (tag)
    term = "Product manufacturer"
    route = generate_route(tag, term)
    print(route)
    for key in route:
        if check_term_availability(term, route[key]) == True:
            print("available")
