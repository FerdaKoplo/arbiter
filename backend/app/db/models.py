from __future__ import annotations

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
from sqlalchemy import func


from datetime import datetime
import enum
from typing import List

from sqlalchemy import (
    String,
    Text,
    Float,
    ForeignKey,
    DateTime,
    Enum as SAEnum,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


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

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    claims: Mapped[List["Claim"]] = relationship(back_populates="document")


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    claim_type: Mapped[ClaimType] = mapped_column(SAEnum(ClaimType), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    scope: Mapped[str | None] = mapped_column(String(255), nullable=True)

    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    document: Mapped["Document"] = relationship(back_populates="claims")

    outgoing_relations: Mapped[List["ClaimRelation"]] = relationship(
        foreign_keys="ClaimRelation.from_claim_id",
        back_populates="from_claim",
    )

    incoming_relations: Mapped[List["ClaimRelation"]] = relationship(
        foreign_keys="ClaimRelation.to_claim_id",
        back_populates="to_claim",
    )


class ClaimRelation(Base):
    __tablename__ = "claim_relations"

    id: Mapped[int] = mapped_column(primary_key=True)

    from_claim_id: Mapped[int] = mapped_column(ForeignKey("claims.id"), nullable=False)
    to_claim_id: Mapped[int] = mapped_column(ForeignKey("claims.id"), nullable=False)

    relation_type: Mapped[RelationType] = mapped_column(
        SAEnum(RelationType), nullable=False
    )
    strength: Mapped[float] = mapped_column(Float, default=1.0)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    from_claim: Mapped["Claim"] = relationship(
        foreign_keys=[from_claim_id], back_populates="outgoing_relations"
    )
    to_claim: Mapped["Claim"] = relationship(
        foreign_keys=[to_claim_id], back_populates="incoming_relations"
    )

    __table_args__ = (
        UniqueConstraint("from_claim_id", "to_claim_id", "relation_type"),
    )


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    options: Mapped[List["DecisionOption"]] = relationship(
        back_populates="decision", cascade="all, delete-orphan"
    )


class DecisionOption(Base):
    __tablename__ = "decision_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    decision_id: Mapped[int] = mapped_column(ForeignKey("decisions.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    decision: Mapped["Decision"] = relationship(back_populates="options")

    claim_links: Mapped[List["DecisionClaimLink"]] = relationship(
        back_populates="option"
    )


class DecisionClaimLink(Base):
    __tablename__ = "decision_claim_links"

    id: Mapped[int] = mapped_column(primary_key=True)

    option_id: Mapped[int] = mapped_column(
        ForeignKey("decision_options.id"), nullable=False
    )
    claim_id: Mapped[int] = mapped_column(ForeignKey("claims.id"), nullable=False)

    effect: Mapped[ClaimEffect] = mapped_column(SAEnum(ClaimEffect), nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    option: Mapped["DecisionOption"] = relationship(back_populates="claim_links")
    claim: Mapped["Claim"] = relationship()

    __table_args__ = (UniqueConstraint("option_id", "claim_id", "effect"),)
