"""
schemas/event.py

Normalized Security Event Schema

Every security tool (Trivy, Falco, Gateway, MCP, Cert Guardian, etc.)
is normalized into this structure before entering the
Deterministic Governance Core.

Author: SEIR AI Platform Engineering
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


#
# Enumerations
#

class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    SUPPRESSED = "suppressed"


class EventSource(str, Enum):
    TRIVY = "trivy"
    FALCO = "falco"
    KUBE_BENCH = "kube-bench"
    PROWLER = "prowler"
    GATEWAY = "gateway"
    CERT_GUARDIAN = "cert_guardian"
    MCP_GUARDIAN = "mcp_guardian"
    DGC = "dgc"
    USER = "user"


#
# Security Event
#

class SecurityEvent(BaseModel):
    """
    Universal event object used throughout the DGC.

    All scanners, agents and gateways should be normalized
    into this model before any policy evaluation occurs.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )

    #
    # Identity
    #

    event_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique Event Identifier"
    )
    
    request_id: str | None = Field(
        default=None,
        description="Original MCP request identifier."
    )

    correlation_id: str | None = Field(
        default=None,
        description="Groups related events into a single transaction or workflow."
    )

    parent_event_id: str | None = Field(
        default=None,
        description="Parent event if this event was generated from another event."
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC Timestamp"
    )

    #
    # Source
    #

    source: EventSource

    scanner_version: str | None = None

    #
    # Classification
    #

    event_type: str = Field(
        description="Normalized event classification"
    )

    severity: Severity

    status: EventStatus = EventStatus.NEW

    #
    # Kubernetes Context
    #

    cluster: str

    namespace: str | None = None

    workload: str | None = None

    pod: str | None = None

    container: str | None = None

    node: str | None = None

    #
    # Cloud Context
    #

    cloud_provider: str | None = None

    account_id: str | None = None

    region: str | None = None

    #
    # Asset Information
    #

    asset: str

    asset_type: str

    #
    # Description
    #

    title: str

    description: str

    #
    # Evidence
    #

    evidence: dict[str, Any] = Field(default_factory=dict)

    metadata: dict[str, Any] = Field(default_factory=dict)

    #
    # Tags
    #

    tags: list[str] = Field(default_factory=list)
