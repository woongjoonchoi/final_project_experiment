from sqlalchemy.orm import Session
from ..schema import models, schemas

# 사용자가 스크랩 정보를 관리한다.
class Managenewsscrap():

    # 유저가 뉴스 스크랩 생성
    def create_news_scrap(db: Session, news_scrap: schemas.NewsScrapCreate):
        db_news_scrap = models.NewsScrap(**news_scrap.dict())
        db.add(db_news_scrap)
        db.commit()
        db.refresh(db_news_scrap)
        return db_news_scrap


    # 유저가 뉴스 스크랩 제거
    def delete_news_scrap(db: Session, news_scrap: schemas.NewsScrapDelete):
        db_news_scrap = models.NewsScrap(**news_scrap.dict())
        db.delete(db_news_scrap)
        db.commit()
        db.refresh(db_news_scrap)
        return db_news_scrap

    pass
