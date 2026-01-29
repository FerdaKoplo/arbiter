from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.domain.services.decision_engine import evaluate_decision
from app.domain.services.document_processor import process_and_save_document

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


@app.post("/documents/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    decision_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    background_tasks.add_task(process_and_save_document, db, file, decision_id)

    return {
        "filename": file.filename,
        "status": "processing_started",
        "linked_to_decision": decision_id,
    }
