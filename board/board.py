from typing import Optional
from fastapi import FastAPI
import uvicorn
import json
import time
from pydantic import BaseModel
# from retrieval import *
from elasticsearch import Elasticsearch , helpers
import index_settings

## You Must need Elastic db using mbn_wiki
INDEX_SETTINGS = index_settings.INDEX_SETTINGS
INDEX_NAME = index_settings.INDEX_NAME

try:
    es.transport.close()
except:
    pass
es = Elasticsearch()
app=FastAPI()
if es.indices.exists(INDEX_NAME):
    pass
@app.get("/board")
def read_news(skip: int = 0 , limit : int = 10) :
    query = "사랑하지만 힘들어 죽겠네"
    res = es.search(index=INDEX_NAME, q=query, size=10)

    return res

if __name__ =='__main__' :
    uvicorn.run(app,host="0.0.0.0" , port=8000)
