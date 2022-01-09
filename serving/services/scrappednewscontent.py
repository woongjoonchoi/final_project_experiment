from sqlalchemy.orm import Session
from schema.models import UserInput, NewsScrap

from elasticsearch import Elasticsearch

es = Elasticsearch()

# 스크랩된 news 기사 본문 가져오기
class Scrappednewscontent():
    # 스크랩된 뉴스 기사 내용과 사용자 입력 내용 불러오기
    def get_scrapped_news(db: Session, news_id: str, user_id: str):
        
        news_content = es.get(index = "news_wiki_index", id=news_id)
        news_scrap = db.query(NewsScrap).filter(NewsScrap.user_news_id == news_id, NewsScrap.user_id == user_id).first()
        user_input = db.query(UserInput).filter(UserInput.user_id == news_id, UserInput.user_id == user_id).first()

        return news_content["_source"], news_scrap, user_input
