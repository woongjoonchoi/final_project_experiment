

from ..schema import schemas , models
from sqlalchemy.orm import Session
# 사용자가 스크랩한 뉴스기사 목록 불러오기
class Scrappedboard():

    # 사용자가 스크랩한 뉴스 기사 제목 리스트 불러오기
    def get_user_news(self,db,owner_user_id) :
        news = db.query(models.NewsScrap).filter(models.NewsScrap.user_id==owner_user_id).all()
        return news    
    