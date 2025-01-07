from typing import List

from database import Transaction
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import TransactionBase, TransactionModel, db_dependency

app = FastAPI()

origins = ["http://localhost:3000"]  # for react

app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.post("/transactions/", response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    # map domain model to db table
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.get("/transactions", response_model=List[TransactionModel])
async def read_transactions(db: db_dependency, skip: int = 0, limit: int = 100):
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
