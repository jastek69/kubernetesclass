"""
schemas/evidence.py

Deterministic Governance Core (DGC)

Evidence Schema

Represents immutable evidence collected from scanners,
gateways, Kubernetes, cloud providers, or AI agents.

Evidence objects are metadata describing where evidence is
stored. Large artifacts remain in external storage.

Default retention for the educational lab is one year.
Organizations may extend this to meet regulatory requirements.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

#
# Default Retention
#

DEFAULT_RETENTION_DAYS = 365


#
# Evidence Type
#

class EvidenceType(str, Enum):

    JSON = "json"

    YAML = "yaml"

    LOG = "log"

    API_RESPONSE = "api_response"

    CERTIFICATE = "certificate"

    IMAGE = "image"

    PDF = "pdf"

    TEXT = "text"


#
# Evidence Source
#

class EvidenceSource(str, Enum):

    TRIVY = "trivy"

    FALCO = "falco"

    KUBE_BENCH = "kube-bench"

    PROWLER = "prowler"

    GATEWAY = "gateway"

    MCP = "mcp"

    CERT_GUARDIAN = "cert_guardian"

    MCP_GUARDIAN = "mcp_guardian"

    USER = "user"

    DGC = "dgc"


#
# Evidence
#

class Evidence(BaseModel):

    model_config = ConfigDict(

        extra="forbid",

        validate_assignment=True,

        use_enum_values=True,
    )

    #
    # Identity
    #

    evidence_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique Evidence Identifier"
    )

    collected_time: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when evidence was collected."
    )

    retention_until: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=DEFAULT_RETENTION_DAYS),
        description="Evidence retention expiration."
    )

    #
    # Relationships
    #

    event_id: str = Field(
        description="Associated SecurityEvent."
    )

    correlation_id: str | None = Field(
        default=None,
        description="Workflow correlation identifier."
    )

    #
    # Source
    #

    source: EvidenceSource

    evidence_type: EvidenceType

    #
    # Artifact
    #

    artifact_name: str = Field(
        description="Original artifact filename."
    )

    artifact_hash: str = Field(
        description="SHA-256 hash of the artifact."
    )

    mime_type: str = Field(
        description="MIME type of the artifact."
    )

    size_bytes: int = Field(
        ge=0,
        description="Artifact size in bytes."
    )

    #
    # Storage
    #

    storage_uri: str = Field(
        description="URI where the artifact is stored."
    )

    #
    # Evidence Content
    #

    raw_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional structured data extracted from the artifact."
    )

    #
    # Metadata
    #

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional evidence metadata."
    )

    #
    # Tags
    #

    tags: list[str] = Field(
        default_factory=list,
        description="Evidence classification tags."
    )
