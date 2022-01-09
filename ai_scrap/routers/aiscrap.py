from fastapi import FastAPI, APIRouter , Depends , Request
from pydantic import BaseModel
from database import engine , SessionLocal
import schemas , models
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import uvicorn

# from services.aiscrappedboard import Aiscrappedboard

models.Base.metadata.create_all(engine)
router = APIRouter(prefix="/aiscrap", tags=["AIScrap"])
templates = Jinja2Templates(directory='./dist')
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally : 
        db.close()
@router.post('/{owner_user_id}')
def create(request : schemas.AINewsScrap,  db : Session = Depends(get_db)):
    new_blog = models.AINewsScrap(user_id = request.owner_user_id , ai_news_id = request.ai_news_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
# AI scrap 페이지로 이동(웅준)
@router.get("/{owner_user_id}")
def get_aiscrap_page(request : Request , owner_user_id ,  db : Session = Depends(get_db)):

    news = db.query(models.AINewsScrap).filter(models.AINewsScrap.user_id==owner_user_id).all()
    print(news[0].user_id)
    # 로그인이 되어있으면 Aiscrappedboard Service 객체로 AI가 스크랩한 뉴스기사 목록 불러오기
    return templates.TemplateResponse('aiscrap.html', context={'request': request , 'ai_news' : news})
    return news
    # 로그인이 안되어있으면 로그인 화면으로 이동(로그인 기능이 구현되어 있다면)
    