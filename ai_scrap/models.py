from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base 



class Blog(Base) :
    __tablename__ = 'blogs'
    id = Column(Integer , primary_key= True , index = True)
    title = Column(String)
    body = Column(String)
class User(Base):
    
    # 테이블의 이름
    __tablename__ = "users"
    id = Column(Integer)
    user_id = Column(String, primary_key=True, index=True) # index?
    hashed_password = Column(String)
    name = Column(String, index=True)
    alarm = Column(Boolean, default=False) # 일단 Boolean


# 관리자 : 관리자아이디(PK) 비밀번호
class Admin(Base):

    __tablename__ = "admins"
    id = Column(Integer)
    admin_id = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)


# UserNews : 유저뉴스아이디(PK) 제목 내용 admin아이디(FK)
# 모든 유저가 볼 수 있는 뉴스
class UserNews(Base):

    __tablename__ = "user_newss"
    id = Column(Integer)
    user_news_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    article = Column(String, index=True)
    admin_id = Column(String, ForeignKey("admins.id")) # 옵션 처리!


# UserInput : 유저질문문장 유저아이디(FK) 뉴스아이디(FK)
# 유저가 입력한 question 관리
class UserInput(Base):

    __tablename__ = "user_input"
    id = Column(Integer , primary_key= True , index = True)
    user_id = Column(String, ForeignKey("users.id"))
    user_news_id = Column(Integer, ForeignKey("user_newss.id"))
    user_input = Column(String, index=True)


# NewsScrap : 유저아이디(FK) 유저뉴스아이디(FK)
# 유저가 뉴스 스크랩한 뉴스
class NewsScrap(Base):

    __tablename__ = "news_scraps"
    id = Column(Integer , primary_key= True , index = True)
    user_id = Column(String, ForeignKey("users.id"))
    user_news_id = Column(Integer, ForeignKey("user_newss.id"))


# AINewsScrap : 유저아이디(FK) AI뉴스아이디(FK)
# AI가 스크랩한 뉴스
class AINewsScrap(Base):

    __tablename__ = "ai_news_scraps"
    id = Column(Integer , primary_key= True , index = True)
    user_id = Column(String, ForeignKey("users.id"))
    ai_news_id = Column(Integer, ForeignKey("user_newss.id"))


# AIInput : AI답변문장 유저아이디(FK) AI뉴스아이디(KF)
# AI가 내놓은 답변
class AIInput(Base):

    __tablename__ = "ai_inputs"
    id = Column(Integer , primary_key= True , index = True)
    ai_input = Column(String, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    ai_news_id = Column(Integer, ForeignKey("user_newss.id"))
