from sqlalchemy.orm import Session
from fastapi import Form

from ..schema import models, schemas

# 사용자가 입력한 정보를 관리한다.
class Manageuserinput():

    # 사용자가 입력한 정보를 DB에 저장하기
    def insert_news_input(db: Session, user_info=schemas.UserInputBase, input: str = Form(...)):
        db_user_input = models.UserInput(**user_info.dict(), user_input=input)
        
        db.add(db_user_input)
        db.commit()
        db.refresh(db_user_input)

        return db_user_input


    # 사용자가 입력한 정보를 DB에서 삭제하기
    def delete_news_input(db: Session, user_input: schemas.UserInputBase):
        pass

    pass