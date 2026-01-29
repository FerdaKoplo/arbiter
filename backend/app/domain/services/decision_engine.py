from typing import List
from dataclasses import dataclass
from sqlalchemy.orm import Session
import time
import random

from app.db.models import Document
from app.domain.repository import DecisionRepository
from app.core.scoring import score_option_with_propagation
from app.core.gemini import extract_claims_from_text

import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.core.gemini import extract_claims_from_text


@dataclass
class OptionScore:
    option_id: int
    score: float
    reasons: list[str]


@dataclass
class DecisionResult:
    decision_id: int
    ranked_options: List[OptionScore]


def gemini_worker(doc_text, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            output = extract_claims_from_text(doc_text)
            return [(c.claim_text[:80], c.confidence) for c in output.claims]

        except Exception as e:
            error_str = str(e)

            if any(
                code in error_str
                for code in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]
            ):
                attempt += 1
                if attempt >= retries:
                    return f"GEMINI ERROR: Failed after {retries} retries. Last error: {error_str}"

                wait_time = (2**attempt) * 2 + random.uniform(0, 1)
                print(
                    f"Gemini busy/limited (Error {error_str[:3]}). Retrying in {wait_time:.2f}s..."
                )
                time.sleep(wait_time)
            else:
                return f"GEMINI ERROR: {error_str}"

    return "GEMINI ERROR: Failed for unknown reasons"


async def evaluate_decision(decision_id: int, db: Session):
    repo = DecisionRepository(db)
    options = repo.get_options(decision_id)

    decision_docs = db.query(Document).filter(Document.decision_id == decision_id).all()
    decision_doc_texts = [d.content for d in decision_docs]

    results = []

    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=4)

    for option in options:
        links = repo.get_links_for_option(option.id)
        score, reasons = score_option_with_propagation(links)

        option_doc_texts = repo.get_documents_for_option(option.id)

        all_texts_to_check = option_doc_texts + decision_doc_texts

        tasks = [
            loop.run_in_executor(executor, gemini_worker, doc_text)
            for doc_text in all_texts_to_check
        ]

        gemini_results = await asyncio.gather(*tasks)

        for result in gemini_results:
            if isinstance(result, list):
                for claim_text, conf in result:
                    reasons.append(f"GEMINI: {claim_text}... => {conf:.3f}")
            else:
                reasons.append(result)

        results.append(OptionScore(option_id=option.id, score=score, reasons=reasons))

    results.sort(key=lambda x: x.score, reverse=True)
    return DecisionResult(decision_id=decision_id, ranked_options=results)
