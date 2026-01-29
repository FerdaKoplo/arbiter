from sqlalchemy.orm import Session
from app.db.models import Claim, Document
from app.core.gemini import extract_claims_from_text


def add_claims_from_text(db: Session, document_id: int, text: str):
    output = extract_claims_from_text(text)

    claims = []
    for c in output.claims:
        claim = Claim(
            text=c.claim_text,
            normalized_text=c.normalized_text,
            confidence=c.confidence,
            claim_type=c.claim_type,
            document_id=document_id,
        )
        db.add(claim)
        claims.append(claim)

    db.commit()
    return claims
