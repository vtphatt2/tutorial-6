"""Read-only demo endpoints: the assignment feature is NOT implemented here."""
from fastapi import APIRouter, Depends
from src.api.auth import Actor, get_current_actor
from src.api.dependencies import get_seed_store
from src.repository.seed_store import SeedStore

router = APIRouter(prefix="/demo", tags=["demo"])


@router.get("/jobs")
def list_jobs(
    actor: Actor = Depends(get_current_actor), store: SeedStore = Depends(get_seed_store)
) -> list[dict[str, str | None]]:
    jobs = store.list_jobs()
    if actor.role == "technician":
        tech = store.find_technician(actor.email)
        jobs = [j for j in jobs if tech is not None and j.assignee_id == tech.id]
    return [{"id": str(j.id), "status": j.status, "site_address": j.site_address,
             "assignee_id": str(j.assignee_id) if j.assignee_id else None} for j in jobs]


@router.get("/technicians")
def list_technicians(
    actor: Actor = Depends(get_current_actor), store: SeedStore = Depends(get_seed_store)
) -> list[dict[str, str]]:
    if actor.role != "manager":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return [{"id": str(t.id), "email": t.email, "availability": t.availability}
            for t in store.list_technicians()]
