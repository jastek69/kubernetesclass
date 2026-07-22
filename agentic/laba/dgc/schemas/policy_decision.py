"""
schemas/policy_decision.py

Deterministic Governance Core (DGC)

Policy Decision Schema

Represents the outcome of evaluating a single policy against
a SecurityEvent.

This object is produced by the Policy Engine and later
consumed by the Decision Engine.
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


#
# Decision Status
#

class PolicyDecisionStatus(str, Enum):

    PASSED = "passed"

    FAILED = "failed"

    WARNING = "warning"

    SKIPPED = "skipped"

    ERROR = "error"


#
# Policy Decision
#

class PolicyDecision(BaseModel):

    model_config = ConfigDict(

        extra="forbid",

        validate_assignment=True,

        use_enum_values=True,
    )

    #
    # Identity
    #

    policy_decision_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique Policy Decision Identifier."
    )

    evaluated_time: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the policy evaluation completed."
    )

    #
    # Relationships
    #

    event_id: str = Field(
        description="Associated SecurityEvent."
    )

    policy_id: str = Field(
        description="Policy evaluated."
    )

    correlation_id: str | None = Field(
        default=None,
        description="Workflow correlation identifier."
    )

    #
    # Classification
    #

    status: PolicyDecisionStatus = Field(
        description="Outcome of the policy evaluation."
    )

    severity: str = Field(
        description="Severity assigned by the policy."
    )

    #
    # Evaluation Result
    #

    passed: bool = Field(
        description="True if the policy evaluation succeeded."
    )

    score: int = Field(
        default=100,
        ge=0,
        le=100,
        description="Policy evaluation score."
    )

    rationale: str = Field(
        description="Human-readable explanation of the evaluation."
    )

    #
    # Evidence
    #

    evidence_ids: list[str] = Field(
        default_factory=list,
        description="Evidence supporting this evaluation."
    )

    #
    # Evaluation Details
    #

    evaluator: str = Field(
        description="Evaluator module used."
    )

    evaluator_version: str = Field(
        default="1.0",
        description="Evaluator version."
    )

    execution_time_ms: float = Field(
        ge=0,
        description="Evaluation execution time."
    )

    #
    # Metadata
    #

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional evaluation metadata."
    )

    #
    # Tags
    #

    tags: list[str] = Field(
        default_factory=list,
        description="Classification tags."
    )
