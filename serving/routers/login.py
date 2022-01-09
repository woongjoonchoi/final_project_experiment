from fastapi import FastAPI, APIRouter, Request, File, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import List

from ..services.managelogin import Checklogin, Signup

from .home import get_db, get_home_page
from ..schema import schemas
from sqlalchemy.orm import Session


router = APIRouter(prefix="/login", tags=["login"])
templates = Jinja2Templates(directory='serving/templates')



# 로그인 페이지로 이동
@router.get("/", description="로그인하는 html 부름")
def get_login_page(request: Request):
    return templates.TemplateResponse('login_form.html', context={'request': request})


# 로그인 하기
    
    # Checklogin Service 객체로 로그인 정보 확인하기

    # 로그인에 성공하면 홈페이지로 이동 -> X

    # 로그인에 실패하면 실패이유 반환하기 -> O

# 비밀번호 이슈 있음
@router.post("/", description="회원가입할 때 이미 등록된 아이디인지 확인해서 있으면 400에러 없으면 해당 아이디 생성")
def login(request: Request, user_id: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = Checklogin.login_user(db, user_id=user_id, password=password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="해당 유저를 찾을 수 없습니다.")
    Checklogin.login_user(db, user_id=user_id, password=password), {"정상적으로 로그인 되었습니다."}
    return get_home_page(request, user_id)

    # 위에 작동이 안 되면 위에 2줄 주석처리하고 아래로 주석 풀어서 로그인 되는지 확인 가능
    # return Checklogin.login_user(db, user_id=user_id, password=password), {"정상적으로 로그인 되었습니다."}


# 회원가입 페이지로 이동
@router.get("/signup", description="유저 회원가입")
def get_signup_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('create_user_form.html', context={'request': request})


# 회원가입 하기
@router.post("/signup", description="회원가입할 때 이미 등록된 아이디인지 확인해서 있으면 400에러 없으면 해당 아이디 생성")
def create_user(request: Request, user_id: str = Form(...), password: str = Form(...), name: str = Form(...), alarm: bool = Form(...), db: Session = Depends(get_db)):
    # Signup Service 객체로 입력받은 회원정보를 db에 저장하기
    db_user = Checklogin.get_user(db, user_id=user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 아이디 입니다.")
    Signup.create_user(db, user_id=user_id, password=password, name=name, alarm=alarm)
    return get_login_page(request=request)



# # 회원탈퇴 페이지로 이동
# # delete_user 해결 못 함
# @router.get("/delete_user", description="탈퇴하는 html 부름")
# def get_delete_user_form(request: Request, db: Session = Depends(get_db)):
#     return templates.TemplateResponse('delete_user_form.html', context={'request': request})



# # 회원탈퇴 하기
# # 추후 users/{user_id}/delete 이런 식으로 넣을 예정
# @router.delete("/delete_user", description="유저 로그인한 경우 회원아이디는 그대로 있고 password 입력해서 탈퇴")
# def delete_user(request: Request, user_id: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
#     db_user = Checklogin.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=400, detail="해당 유저를 찾을 수 없습니다.")

#     db_user = Checklogin.login_user(db, user_id=user_id, password=password)
#     if db_user is None:
#         raise HTTPException(status_code=400, detail="비밀번호가 틀렸습니다.")
#     Signup.delete_user(db=db, user_id=user_id, password=password)
#     return templates.TemplateResponse('login_form.html', context={'request': request})



if __name__ == '__main__':
    app = FastAPI()
    app.include_router(router)
    uvicorn.run(app="AIPaperboy:app", host="0.0.0.0", port=8000, reload=True)
