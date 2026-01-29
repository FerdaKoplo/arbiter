import os
import shutil
from fastapi import UploadFile
from pdfminer.high_level import extract_text
from sqlalchemy.orm import Session
from app.db.models import Document

UPLOAD_DIR = "storage/pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def process_and_save_document(db: Session, file: UploadFile, decision_id: int):
    file_location = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text_content = extract_text(file_location)
    except Exception as e:
        print(f"Extraction failed: {e}")
        text_content = "Error extraction text from PDF."

    db_doc = Document(
        title=file.filename,
        source="upload",
        content=text_content,
        decision_id=decision_id,
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    return db_doc
