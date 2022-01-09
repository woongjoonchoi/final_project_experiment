from sqlalchemy.orm import Session
from ..schema import models, schemas


# 로그인 정보 확인하기
class Checklogin():

    # 사용자가 입력한 로그인 정보가 정확한지 확인하기

    # User : 유저아이디(PK) 비밀번호 이름 알람설정
    # 필터로 내가 선택한 유저만
    def get_user(db: Session, user_id: str):
        return db.query(models.User).filter(models.User.user_id == user_id).first()


    # 아이디 비밀번호 줘서 로그인
    def login_user(db: Session, user_id: str, password: str):
        fake_hashed_password = password + "notreallyhashed"
        return db.query(models.User).filter(models.User.user_id == user_id and models.User.password == fake_hashed_password).first()


    # # 모든 유저
    # def get_users(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.User).offset(skip).limit(limit).all()



# 회원가입 하기, 회원탈퇴 하기
class Signup():

    # Signup Service 객체로 입력받은 회원정보를 db에 저장하기

    # 유저 직접 만듦
    def create_user(db: Session, user_id: str, password: str, name: str, alarm: bool):
        fake_hashed_password = password + "notreallyhashed"
        db_user = models.User(user_id=user_id, hashed_password=fake_hashed_password, name=name, alarm=alarm)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


    # Signup Service 객체로 입력받은 회원정보를 db에 저장하기

    # 유저 직접 삭제
    def delete_user(db: Session, user_id: str, password: str):
        fake_hashed_password = password + "notreallyhashed"
        db_user = models.User(user_id=user_id, hashed_password=fake_hashed_password)
        db.delete(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user



