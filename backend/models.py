from typing import Annotated

from database import Base, SessionLocal, engine
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session


# It does feel redundant to have two model definitions (one for Pydantic, one for database)
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str


class TransactionModel(TransactionBase):
    id: int

    class Config:
        org_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


Base.metadata.create_all(bind=engine)
