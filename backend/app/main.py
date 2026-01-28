from app.db.session import SessionLocal
from app.domain.services.decision_engine import evaluate_decision

if __name__ == "__main__":
    db = SessionLocal()
    result = evaluate_decision(decision_id=1, db=db)

    print("Decision:", result.decision_id)
    for r in result.ranked_options:
        print("Option", r.option_id, "=>", r.score)
        for reason in r.reasons:
            print("   ", reason)
