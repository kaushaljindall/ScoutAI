from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import Field


class BaseDocument(Document):
    """
    Base Beanie Document. Beanie automatically manages `id` as PydanticObjectId.
    We store it as string for easy serialization.
    """
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[str] = None
    is_deleted: bool = False

    class Settings:
        use_revision = False
