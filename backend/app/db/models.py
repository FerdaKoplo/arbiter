from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    ForeignKey,
    DateTime,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
import enum


class ClaimType(enum.Enum):
    empirical = "empirical"
    theoretical = "theoretical"
    opinion = "opinion"


class RelationType(enum.Enum):
    supports = "supports"
    contradicts = "contradicts"
    refines = "refines"
    assumes = "assumes"


class ClaimEffect(enum.Enum):
    supports = "supports"
    weakens = "weakens"
    blocks = "blocks"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    source = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    claims = relationship("Claim", back_populates="document")


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

    normalized_text = Column(Text, nullable=True)

    claim_type = Column(Enum(ClaimType), nullable=False)

    confidence = Column(Float, default=0.5)

    scope = Column(String(255), nullable=True)

    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="claims")

    outgoing_relations = relationship(
        "ClaimRelation",
        foreign_keys="ClaimRelation.from_claim_id",
        back_populates="from_claim",
    )

    incoming_relations = relationship(
        "ClaimRelation",
        foreign_keys="ClaimRelation.to_claim_id",
        back_populates="to_claim",
    )


class ClaimRelation(Base):
    __tablename__ = "claim_relations"

    id = Column(Integer, primary_key=True)

    from_claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    to_claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)

    relation_type = Column(Enum(RelationType), nullable=False)

    strength = Column(Float, default=1.0)  # optional weighting

    created_at = Column(DateTime, default=datetime.utcnow)

    from_claim = relationship(
        "Claim", foreign_keys=[from_claim_id], back_populates="outgoing_relations"
    )
    to_claim = relationship(
        "Claim", foreign_keys=[to_claim_id], back_populates="incoming_relations"
    )

    __table_args__ = (
        UniqueConstraint("from_claim_id", "to_claim_id", "relation_type"),
    )


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    options = relationship(
        "DecisionOption", back_populates="decision", cascade="all, delete-orphan"
    )


class DecisionOption(Base):
    __tablename__ = "decision_options"

    id = Column(Integer, primary_key=True)

    decision_id = Column(Integer, ForeignKey("decisions.id"), nullable=False)

    name = Column(String(255), nullable=False)  # e.g. "Use PostgreSQL"

    created_at = Column(DateTime, default=datetime.utcnow)

    decision = relationship("Decision", back_populates="options")

    claim_links = relationship("DecisionClaimLink", back_populates="option")


class DecisionClaimLink(Base):
    __tablename__ = "decision_claim_links"

    id = Column(Integer, primary_key=True)

    option_id = Column(Integer, ForeignKey("decision_options.id"), nullable=False)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)

    effect = Column(Enum(ClaimEffect), nullable=False)

    weight = Column(Float, default=1.0)

    created_at = Column(DateTime, default=datetime.utcnow)

    option = relationship("DecisionOption", back_populates="claim_links")
    claim = relationship("Claim")

    __table_args__ = (UniqueConstraint("option_id", "claim_id", "effect"),)
