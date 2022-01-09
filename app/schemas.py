from pydantic import BaseModel
from uuid import UUID


class Question(BaseModel):

    id: UUID
    text: str