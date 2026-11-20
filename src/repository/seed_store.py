"""Disposable data for the lab; no PostgreSQL installation required."""
from dataclasses import replace
from threading import RLock
from uuid import UUID

from src.domain.seed_models import SeedJob, SeedTechnician

JOB_A = UUID("00000000-0000-0000-0000-000000000101")
JOB_B = UUID("00000000-0000-0000-0000-000000000102")
TECH_A = UUID("00000000-0000-0000-0000-000000000201")
TECH_B = UUID("00000000-0000-0000-0000-000000000202")


class SeedStore:
    """Per-application mutable state. Repository adapters may use this store."""

    def __init__(self) -> None:
        self.lock = RLock()
        self.jobs: dict[UUID, SeedJob] = {
            JOB_A: SeedJob(JOB_A, "12 Main Street", "Broken air conditioner", "high", "unassigned"),
            JOB_B: SeedJob(JOB_B, "87 Elm Street", "Leaking pipe", "medium", "unassigned"),
        }
        self.technicians: dict[UUID, SeedTechnician] = {
            TECH_A: SeedTechnician(TECH_A, "alex@fieldco.com", "Alex", "AVAILABLE"),
            TECH_B: SeedTechnician(TECH_B, "sam@fieldco.com", "Sam", "ON_LEAVE"),
        }

    def get_job(self, job_id: UUID) -> SeedJob | None:
        with self.lock:
            return self.jobs.get(job_id)

    def list_jobs(self) -> list[SeedJob]:
        with self.lock:
            return list(self.jobs.values())

    def list_technicians(self) -> list[SeedTechnician]:
        with self.lock:
            return list(self.technicians.values())

    def find_technician(self, email: str) -> SeedTechnician | None:
        with self.lock:
            return next((t for t in self.technicians.values() if t.email == email), None)

    def update_job(self, job_id: UUID, assignee_id: UUID) -> SeedJob | None:
        with self.lock:
            previous = self.jobs.get(job_id)
            if previous is None:
                return None
            updated = replace(previous, assignee_id=assignee_id, status="assigned")
            self.jobs[job_id] = updated
            return updated
