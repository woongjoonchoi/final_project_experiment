from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Session
from ...code import predict


# Batch serving 하기 : 뉴스 기사를 업로드하기, 사용자 질문 정보 불러오기, 모델로 예측하기, 결과값 저장하기
class Batchserving():

    def serving(db: Session):
        Table_name = "user_input"
        questions = db.query(Table_name).all()

        model, tokenizer = predict.load_model()
        prediction = predict.get_prediction(model, tokenizer, questions)

        return prediction