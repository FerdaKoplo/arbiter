from dotenv import load_dotenv
from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.models import Decision, DecisionOption
from app.db.session import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from app.domain.services.decision_engine import evaluate_decision
from app.domain.services.document_processor import process_and_save_document
from app.lib.get_env import get_env_variable

load_dotenv()

app = FastAPI()


origins = get_env_variable("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DecisionCreate(BaseModel):
    title: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/decisions")
def create_decision(decision_in: DecisionCreate, db: Session = Depends(get_db)):
    new_decision = Decision(title=decision_in.title, description="User created project")
    db.add(new_decision)
    db.commit()
    db.refresh(new_decision)

    opt1 = DecisionOption(decision_id=new_decision.id, name="Option A (Proceed)")
    opt2 = DecisionOption(decision_id=new_decision.id, name="Option B (Status Quo)")
    opt3 = DecisionOption(decision_id=new_decision.id, name="Option C (Alternative)")

    db.add_all([opt1, opt2, opt3])
    db.commit()

    return new_decision


@app.get("/decisions/{decision_id}/evaluate")
async def get_decision(decision_id: int, db: Session = Depends(get_db)):
    result = await evaluate_decision(decision_id, db)
    return result


@app.post("/documents/upload")
async def upload_document(
    decision_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    process_and_save_document(db, file, decision_id)

    return {
        "filename": file.filename,
        "status": "processing_started",
        "linked_to_decision": decision_id,
    }


# @app.post("/documents/upload")
# async def upload_document(
#     background_tasks: BackgroundTasks,
#     decision_id: int,
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     background_tasks.add_task(process_and_save_document, db, file, decision_id)
#
#     return {
#         "filename": file.filename,
#         "status": "processing_started",
#         "linked_to_decision": decision_id,
#     }
