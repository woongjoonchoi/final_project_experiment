import uvicorn
from fastapi import FastAPI, APIRouter , Depends , Form
from pydantic import BaseModel
from database import engine , SessionLocal
import schemas , models
from sqlalchemy.orm import Session
from routers import *
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
models.Base.metadata.create_all(engine)



app = FastAPI()
app.mount("/dist/css/", StaticFiles(directory="dist/css"), name="home")

# @app.get("/")
# def get_home_page():
#     return RedirectResponse("./home")

path = './routers/'
file_list = os.listdir(path)
file_list_py = [file.replace('.py', '') for file in file_list if file.endswith('.py')]
file_list_py.remove('__init__')

for name in file_list_py:
    app.include_router(locals()[name].router)
@app.post('/test/')
def test_page(context : str = Form(...) , some_key2 : str = Form(...)):

    return {"context" : context  , "some_key2" : some_key2}
## if 안에서 지역변수 취급 받는듯
if __name__=='__main__' :
    print(dir())


    uvicorn.run(app = "main:app", host = "0.0.0.0" , port = 8000,reload=True )
    # uvicorn.run(app , host = "0.0.0.0" , port =8000)
