"""
schemas/execution_plan.py

Deterministic Governance Core (DGC)

Execution Plan Schema

Represents an immutable execution plan generated from a
Decision.

An ExecutionPlan describes WHAT should happen.

It performs NO actions.

Execution is performed later by the Execution Engine.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from schemas.execution_task import ExecutionTask


class ExecutionPlan(BaseModel):

    model_config = ConfigDict(

        extra="forbid",

        validate_assignment=True,

        use_enum_values=True,

    )

    ####################################################################
    #
    # Identity
    #
    ####################################################################

    plan_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique execution plan identifier."
    )

    created_time: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the execution plan was generated."
    )

    planner_version: str = Field(
        default="1.0",
        description="Execution Planner version."
    )

    ####################################################################
    #
    # Relationships
    #
    ####################################################################

    decision_id: str = Field(
        description="Associated Decision."
    )

    event_id: str = Field(
        description="Associated SecurityEvent."
    )

    correlation_id: str | None = Field(
        default=None,
        description="Workflow correlation identifier."
    )

    ####################################################################
    #
    # Summary
    #
    ####################################################################

    task_count: int = Field(
        default=0,
        ge=0,
        description="Total number of execution tasks."
    )

    ####################################################################
    #
    # Tasks
    #
    ####################################################################

    tasks: list[ExecutionTask] = Field(
        default_factory=list,
        description="Ordered execution tasks."
    )

    ####################################################################
    #
    # Metadata
    #
    ####################################################################

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Planner metadata."
    )

    ####################################################################
    #
    # Tags
    #
    ####################################################################

    tags: list[str] = Field(
        default_factory=list,
        description="Classification tags."
    )
