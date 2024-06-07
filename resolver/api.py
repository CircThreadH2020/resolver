from pydantic import BaseModel, HttpUrl
from fastapi import FastAPI, HTTPException, Request, Depends, Query
from fastapi.staticfiles import StaticFiles

from resolver.tagparser.dbm import DatabaseManagement, Tagstyle
from resolver.tagparser.tagparser import Parser, Tagstyle, AmbiguousTagError, InvalidTagError
import sqlite3

class ResolverResponse(BaseModel):
    url: HttpUrl
    body: dict

description = """
The resolve-Method generates the path to a certain datapoint requested 
by the user by automatically asserting the term with the correct information source. 
It outputs a parametrized URL which points to the information providers API.
"""


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True},
              description=description)

# app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    db = DatabaseManagement()
    yield db

def get_parser():
    parser = Parser()
    yield parser


@app.post("/tags/", tags=["identifier"])
async def add_tag(tag: Tagstyle, db: DatabaseManagement = Depends(get_db)):
    try:
        if db.add_tag(tag):
            return {"status": "Tag added successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="An error occurred while adding the tag")

@app.get("/tags/{tag_id}", response_model=Tagstyle, tags=["identifier"])
async def get_tag(tag_id: int, db: DatabaseManagement = Depends(get_db)):
    tag = db.retrieve_tag_by_id(tag_id)
    if tag:
        return tag
    raise HTTPException(status_code=404, detail="Tag not found")

@app.put("/tags/{tag_id}", tags=["identifier"])
async def update_tag(tag_id: int, updated_tag: Tagstyle, db: DatabaseManagement = Depends(get_db)):
    try:
        if db.update_tag_by_name(tag_id, updated_tag):
            return {"status": "Tag updated successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the tag")

@app.delete("/tags/{tag_id}", tags=["identifier"])
async def delete_tag(tag_id: int, db: DatabaseManagement = Depends(get_db)):
    try:
        if db.delete_tag_by_id(tag_id):
            return {"status": "Tag deleted successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the tag")

@app.delete("/tags", tags=["identifier"])
async def delete_all_tags(db: DatabaseManagement = Depends(get_db)):
    try:
        if db.delete_all_tags():
            return {"status": "All tags deleted successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting all tags")

@app.get("/resolver/", response_model=ResolverResponse, tags=["resolver"])
async def retrieve_url_to_data_endpoint(identifier_content: str, term: str=None, role: str=None, token: str=None):
    return "This method is still work in progress"

@app.get("/healthcheck/", tags=['utils'])
async def conduct_internal_healthcheck():
    return "This method is still work in progress"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=20005)
