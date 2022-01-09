from sqlalchemy.orm import Session
from ..schema.models import UserNews, AIInput, NewsScrap, UserInput
from elasticsearch import Elasticsearch

es = Elasticsearch()

# AI가 스크랩한 뉴스 기사 본문 가져오기
class Aiscrappednewscontent():
    # AI가 스크랩한 뉴스 기사 내용, 사용자 입력 내용, AI 입력 내용 불러오기
    def get_news(db: Session, news_id: str, user_id: str):
        news_content = es.get(index = "news_wiki_index", id=news_id)
        ai_input = db.query(AIInput).filter(AIInput.ai_news_id == news_id, user_id == user_id).first()
        news_scrap = db.query(NewsScrap).filter(NewsScrap.user_news_id == news_id, NewsScrap.user_id == user_id).first()
        user_input = db.query(UserInput).filter(UserInput.user_id == news_id, UserInput.user_id == user_id).first()
        return news_content["_source"], ai_input, news_scrap, user_input
