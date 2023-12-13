from fastapi import FastAPI
from core import parse_tag, generate_route

description = """
The resolve-Method generates the path to a certain datapoint requested 
by the user by automatically asserting the term with the correct information source. 
It outputs a parametrized URL which points to the information providers API.

The method has two query parameters:

* **p_tag**: This is the content of a product identification tag. The resolver 
supports different formats like the GS1 digital link format that can incorporate 
identifiers at the product model and the product unit level (More information 
[here](https://www.gs1.org/standards/gs1-digital-link)) or plain identification 
numbers (GTIN, EAN, serial number, ...).
For testing you can use the following examples:
    * http://circthread.eu/01/18/21/1234567
    * 18
* **term**: This gives the datapoint semantically described through the 
[CircThread vocabulary](https://github.com/CircThreadH2020/ct_product_metadata_vocabulary) 
the user wants to recieve the URL to.
For testing you can use the following example:
    * Product manufacturer

Currently the resolver connects only to the 
[product model metadata catalogue](http://95.60.60.92:5000/swagger/index.html)
"""

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True},
              description=description)


@app.get("/resolver/", tags=["Resolver"])
def resolver_root(p_tag: str, term: str):
    tag = parse_tag(p_tag)
    urls = generate_route(tag, term)

    return urls


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=20005)
