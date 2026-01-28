from sqlalchemy.orm import Session
from app.db import models


class DecisionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_options(self, decision_id: int):
        return (
            self.db.query(models.DecisionOption)
            .filter(models.DecisionOption.decision_id == decision_id)
            .all()
        )

    def get_links_for_option(self, option_id: int):
        return (
            self.db.query(models.DecisionClaimLink)
            .filter(models.DecisionClaimLink.option_id == option_id)
            .all()
        )
