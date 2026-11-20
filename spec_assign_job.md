# Specification: Assign Job to Technician

## Context
Field Repair Tracker API. Layered architecture: FastAPI → Service Layer → Repository Layer → **PostgreSQL in the original tutorial**. This tutorial starter uses an **in-memory repository adapter** so you can focus on the SDLC without provisioning a database. `src/api/auth.py` already validates a demo-signed JWT (training only).

## Endpoint
`POST /jobs/{job_id}/assign`

## Access Control
- Only a user with `role=manager` may assign a job.
- Any other authenticated role receives HTTP 403. Unauthenticated requests receive HTTP 401.

## Request Body
```json
{"assignee_email": "alex@fieldco.com"}
```

## Business Rules
1. The job must exist: return 404 if missing.
2. The technician must exist and have availability `AVAILABLE` **at assignment time**: return 409 otherwise.
3. On success, set `job.assignee_id`, change status to `assigned`, and persist through the repository.
4. After a successful assignment, schedule a notification asynchronously; never wait on the external notification service in the HTTP request path.
5. Failed attempts must not mutate the job or send notifications.

## Success Response (HTTP 200)
```json
{"job_id": "00000000-0000-0000-0000-000000000101", "assignee_email": "alex@fieldco.com", "status": "assigned"}
```

## Error Contract
- 400: missing or malformed request body (FastAPI's default is 422; explicitly adapt if targeting this spec).
- 401: unauthenticated caller.
- 403: authenticated caller is not a manager.
- 404: unknown job.
- 409: technician does not exist or is unavailable.

## Implementation Constraints
- Python 3.12, FastAPI, typed dataclasses for domain entities.
- `src/domain/repair_job.py`: RepairJob and Technician dataclasses.
- `src/repository/job_repository.py`: abstract JobRepository with find_by_id and update_assignee; create a seed-store-backed adapter.
- `src/service/job_service.py`: AssignJobService enforcing business rules with injected dependencies.
- `src/api/job_router.py`: FastAPI route with dependency injection and BackgroundTasks.
- Wire the router into `create_app()` in `src/main.py`.
- Avoid module-level mutable state. Store is per-app and supplied via `get_seed_store`.
- Existing seed data is at `src/repository/seed_store.py` and authentication at `src/api/auth.py`.
- `tests/test_assign_contract.py` defines observable behavior. Add notification tests of your own.

## Deliberate Questions for Students
- Can another manager overwrite an existing assignment? The original brief does not say.
- Should unknown technician and unavailable technician share the same error message?
- How do you ensure transactionality and concurrency if moving to PostgreSQL?
- How would a durable notification queue change the design?

Reference: https://book.agentic-swe.dev/tutorial_6.html (adapted for a self-contained classroom lab).
