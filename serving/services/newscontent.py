from sqlalchemy.orm import Session
from ..schema.models import UserNews, UserInput
from elasticsearch import Elasticsearch

es = Elasticsearch()


# news 기사 본문 가져오기
class Newscontent():

    # 뉴스 기사 내용과 사용자 입력 내용 불러오기
    def get_news(db: Session, news_id: str, user_id: str):
        
        res = es.get(index = "news_wiki_index_update", id=news_id)
        return res["_source"], news_id
