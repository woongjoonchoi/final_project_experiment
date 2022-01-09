from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import tables, schemas
from .database import engine, SessionLocal

import random

app = FastAPI()
templates = Jinja2Templates(directory='./app/script')

tables.Base.metadata.create_all(engine)

@app.get('/')
def login_page(request: Request):
    return templates.TemplateResponse('login_form.html', context={'request': request})

@app.post('/main')
def main_page(request: Request, id: str = Form(...)):
    return templates.TemplateResponse('main_form.html', context={'request': request})

@app.get('/article')
def get_text_form(request: Request):
    return templates.TemplateResponse('article_form.html', context={'request': request})

def get_db():
    db = SessionLocal()

    try:
        yield db
    except:
        db.close()

@app.post('/question')
def question_to_db(text: str = Form(...), db: Session = Depends(get_db)):
    new_question = tables.Question(id=random.randint(0, 1000000), text=text)

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question
