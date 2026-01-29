from sqlalchemy.orm import Session, joinedload
from app.db import models
from typing import List


class DecisionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_options(self, decision_id: int) -> list[models.DecisionOption]:
        return (
            self.db.query(models.DecisionOption)
            .filter(models.DecisionOption.decision_id == decision_id)
            .all()
        )

    def get_links_for_option(self, option_id: int) -> list[models.DecisionClaimLink]:
        return (
            self.db.query(models.DecisionClaimLink)
            .options(
                joinedload(models.DecisionClaimLink.claim)
                .joinedload(models.Claim.outgoing_relations)
                .joinedload(models.ClaimRelation.to_claim)
            )
            .filter(models.DecisionClaimLink.option_id == option_id)
            .all()
        )

    def get_documents_for_option(self, option_id: int) -> List[str]:
        links = self.get_links_for_option(option_id)
        doc_ids = {link.claim.document_id for link in links if link.claim.document_id}

        if not doc_ids:
            return []

        docs = (
            self.db.query(models.Document).filter(models.Document.id.in_(doc_ids)).all()
        )

        return [doc.content for doc in docs if doc.content]
