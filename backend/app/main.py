from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.domain.services.decision_engine import evaluate_decision

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/decisions/{decision_id}")
async def get_decision(decision_id: int, db: Session = Depends(get_db)):
    result = await evaluate_decision(decision_id, db)
    return result
