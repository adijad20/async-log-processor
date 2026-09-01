from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, field_validator


class LogLevel(str, Enum):
    """Supported logging severity levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class LogPayload(BaseModel):
    """Data contract for incoming raw log payloads."""
    client_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique identifier of the sending service",
        examples=["payment-service"]
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the log occurred"
    )
    level: LogLevel = Field(
        ...,
        description="Severity level of the log entry",
        examples=[LogLevel.ERROR]
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Log message content",
        examples=["Failed to connect to external payment gateway"]
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Arbitrary structured contextual information",
        examples=[{"retry_count": 3, "trace_id": "a8f3-4b92"}]
    )

    @field_validator("client_id")
    @classmethod
    def sanitize_client_id(cls, value: str) -> str:
        """Enforces clean lowercase slug format for client IDs."""
        return value.strip().lower()

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_id": "payment-service",
                "timestamp": "2026-08-09T10:30:00Z",
                "level": "ERROR",
                "message": "Failed to connect to Stripe API",
                "metadata": {"retry_count": 3}
            }
        }
    }


class LogIngestResponse(BaseModel):
    """Standardized response schema for accepted logs."""
    status: str = "accepted"
    message: str = "Log accepted for asynchronous processing"
    client_id: str
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))