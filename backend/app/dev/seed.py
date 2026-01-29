import random
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.db.models import (
    Document,
    Claim,
    ClaimRelation,
    Decision,
    DecisionOption,
    DecisionClaimLink,
    ClaimType,
    RelationType,
    ClaimEffect,
)


def seed(db: Session):
    print("Seeding database...")

    print("... Creating Decisions")
    decisions = []
    for i in range(10):
        d = Decision(
            title=f"Decision {i + 1}: Strategic Move",
            description="Synthetic decision scenario for testing.",
        )
        db.add(d)
        decisions.append(d)

    db.commit()

    print("   ... Creating Decision Options")
    options = []
    for d in decisions:
        for j in range(3):
            o = DecisionOption(
                decision=d,
                name=f"Option {j + 1} for {d.title}",
            )
            db.add(o)
            options.append(o)

    db.commit()

    print("... Creating Documents with Context Links")
    docs = []
    for i in range(50):
        assigned_decision_id = None
        if random.random() < 0.3:
            assigned_decision_id = random.choice(decisions).id

        d = Document(
            title=f"Document {i + 1}",
            source="synthetic_seed",
            content=f"This is synthetic document {i + 1}. It contains important claims about the world.",
            decision_id=assigned_decision_id,  # <--- LINKING HERE
        )
        db.add(d)
        docs.append(d)

    db.commit()

    print("   ... Creating Claims")
    claims = []
    for i in range(1000):
        doc = random.choice(docs)

        c = Claim(
            text=f"Claim {i + 1}: something something important",
            normalized_text=None,
            claim_type=random.choice(list(ClaimType)),
            confidence=round(random.uniform(0.3, 0.99), 3),
            scope=None,
            document=doc,
        )
        db.add(c)
        claims.append(c)

    db.commit()

    print(" ... Building Knowledge Graph (Claim Relations)")
    existing = set()
    for _ in range(2000):
        a = random.choice(claims)
        b = random.choice(claims)

        if a.id == b.id:
            continue

        rel_type = random.choice(list(RelationType))

        key = (a.id, b.id, rel_type)
        if key in existing:
            continue

        existing.add(key)

        rel = ClaimRelation(
            from_claim=a,
            to_claim=b,
            relation_type=rel_type,
            strength=round(random.uniform(0.1, 1.0), 3),
        )
        db.add(rel)

    db.commit()

    print("   ... Linking Claims to Decision Options")
    claim_clusters = []
    for i in range(50):
        cluster = random.sample(claims, 10)
        claim_clusters.append(cluster)

    link_existing = set()

    for o in options:
        cluster = random.choice(claim_clusters)

        for cl in cluster:
            effect = random.choices(
                [ClaimEffect.supports, ClaimEffect.weakens, ClaimEffect.blocks],
                weights=[0.6, 0.3, 0.1],
            )[0]

            key = (o.id, cl.id, effect)
            if key in link_existing:
                continue

            link_existing.add(key)

            link = DecisionClaimLink(
                option=o,
                claim=cl,
                effect=effect,
                weight=round(random.uniform(0.5, 1.5), 3),
            )
            db.add(link)

    db.commit()

    print("Seeding complete.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
