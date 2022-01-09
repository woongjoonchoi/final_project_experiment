from fastapi import FastAPI, APIRouter , Depends , Request
from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy.orm import Session


from ..services.scrappedboard import Scrappedboard
from ..services.manageuserinput import Manageuserinput
from ..services.managenewsscrap import Managenewsscrap
from ..schema.database import engine , SessionLocal
from ..schema import models,schemas
from .home import get_db

models.Base.metadata.create_all(engine)
router = APIRouter(prefix="/scrap", tags=["Scrap"])
templates = Jinja2Templates(directory='serving/templates')


# 사용자 scrap 페이지로 이동(웅준)
newsscrapboard = Scrappedboard()

@router.post('/{user_id}')
def create(request : schemas.NewsScrap,  db : Session = Depends(get_db)):
    new_blog = models.NewsScrap(user_id = request.user_id , user_news_id = request.user_news_id , news_scrap_id = request.news_scrap_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
@router.get("/")
def get_scrap_page(request : Request ,  db : Session = Depends(get_db)):
    owner_user_id = "wjc1"
    news = newsscrapboard.get_user_news(db,owner_user_id)
    # owner_user_id=""
    # 로그인이 되어있으면 Scrappedboard Service 객체로 사용자가 스크랩한 뉴스기사 목록 불러오기

    # 로그인이 안되어있으면 로그인 화면으로 이동(로그인 기능이 구현되어 있다면)
    return templates.TemplateResponse('myscrap.html', context={'request': request , 'my_news' : news})
    pass



if __name__ == '__main__':
    app = FastAPI()
    app.include_router(router)
    uvicorn.run(app="AIPaperboy:app", host="0.0.0.0", port=8000, reload=True)
