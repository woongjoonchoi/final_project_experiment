from typing import List, Optional
from pydantic import BaseModel
# 관리자 : 아이디(PK) 비밀번호
class AdminBase(BaseModel):
    id: int


class AdminCreate(AdminBase):
    password: str


class Admin(AdminBase):
    pass

    class Config:
        orm_mode = True


# 뉴스 : 아이디(PK) 제목 내용
class NewsBase(BaseModel):
    title: str
    article: str


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int
    owner_scrap_id: int

    class Config:
        orm_mode = True
class ScrapBase(BaseModel):
    question_sentence: str
    answer_sentence: Optional[str] = None
class AINewsScrap(ScrapBase):
    id: int
    question_news: List[News] = []
    answer_news: List[News] = []
    owner_user_id: int
    ai_news_id : int 
    class Config:
        orm_mode = True
