"""Pre-existing read-only seed models, not the student implementation models."""
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SeedJob:
    id: UUID
    site_address: str
    fault_description: str
    priority: str
    status: str
    assignee_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class SeedTechnician:
    id: UUID
    email: str
    name: str
    availability: str
