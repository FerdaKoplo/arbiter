from typing import List
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.domain.repository import DecisionRepository
from app.core.scoring import score_option


@dataclass
class OptionScore:
    option_id: int
    score: float
    reasons: list[str]


@dataclass
class DecisionResult:
    decision_id: int
    ranked_options: List[OptionScore]


def evaluate_decision(decision_id: int, db: Session) -> DecisionResult:
    repo = DecisionRepository(db)

    options = repo.get_options(decision_id)

    results: list[OptionScore] = []

    for option in options:
        links = repo.get_links_for_option(option.id)

        score, reasons = score_option(links)

        results.append(
            OptionScore(
                option_id=option.id,
                score=score,
                reasons=reasons,
            )
        )

    results.sort(key=lambda x: x.score, reverse=True)

    return DecisionResult(decision_id=decision_id, ranked_options=results)
