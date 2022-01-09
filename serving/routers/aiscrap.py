from fastapi import FastAPI, APIRouter , Depends , Request
from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy.orm import Session
from ..services.aiscrappedboard import Aiscrappedboard
from ..schema.database import engine , SessionLocal
from .home import get_db
from ..schema import models,schemas
from .home import get_db

models.Base.metadata.create_all(engine)
router = APIRouter(prefix="/aiscrap", tags=["AIScap"])
templates = Jinja2Templates(directory='serving/templates')

aiscrapboard =Aiscrappedboard()
# AI scrap 페이지로 이동(웅준)


@router.post('/{user_id}')
def create(request : schemas.AIInput,  db : Session = Depends(get_db)):
    new_blog = models.AIInput(user_id = request.user_id , ai_news_id = request.ai_news_id , ai_input_id = request.ai_input_id, ai_input= request.ai_input)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
@router.get("/")
def get_aiscrap_page(request : Request ,  db : Session = Depends(get_db)):
    owner_user_id = "wjc1"
    news = aiscrapboard.get_user_news(db,owner_user_id)
    # 로그인이 되어있으면 Aiscrappedboard Service 객체로 AI가 스크랩한 뉴스기사 목록 불러오기
    return templates.TemplateResponse('aiscrap.html', context={'request': request , 'ai_news' : news})
    # 로그인이 안되어있으면 로그인 화면으로 이동(로그인 기능이 구현되어 있다면)
    pass


if __name__ == '__main__':
    app = FastAPI()
    app.include_router(router)
    uvicorn.run(app="AIPaperboy:app", host="0.0.0.0", port=8000, reload=True)
