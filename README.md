# Field Repair Tracker — AI-Assisted SDLC Lab (Tutorial 6)

In this tutorial, you will take a vague brief through **requirements → UML design → specification-driven implementation** using an AI assistant. Your main coding task is to implement **Assign Job**. It is **intentionally absent** from the starter.

> Important: This is an educational adaptation, not a production-ready field service system. Tutorial 6 describes PostgreSQL; this starter substitutes a thread-safe, per-application in-memory store to avoid database setup. JWT verification is a simplified local demo and is **not suitable for production**. Other use cases (photo upload, offline sync, reports) are design exercises only, not working APIs.

## 1. Prerequisites

- **Python 3.12** (a Python 3.12+ interpreter that satisfies the project requirement).
- **uv**, from [docs.astral.sh/uv](https://docs.astral.sh/uv/).
- An AI assistant or coding agent. Claude Code is used in the source tutorial, but other agents are fine.
- A terminal and code editor. No Docker or database installation is required.

## 2. Quick Start (Windows PowerShell, macOS, Linux)

Open a terminal in its directory, and run:

```bash
uv sync
uv run pytest tests/test_starter.py -q
uv run uvicorn src.main:app --reload
```

If you do not have Python 3.12, install it with `uv python install 3.12` and repeat. Stop the server using Ctrl+C.

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API docs or check [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health). The health endpoint should return `{"status":"ok"}`.

**The Assign Job endpoint does not exist yet.** This is intentional. Do not expect `uv run pytest tests/test_assign_contract.py -q` to pass before Activity 3.

## 3. Inspect the Running Starter

The application provides two existing read-only APIs:

- `GET /demo/jobs`: managers see all jobs; technicians see only jobs assigned to them.
- `GET /demo/technicians`: managers only.

Sample data is regenerated for each new application instance:

| Kind | ID (last 3 digits) | Value | State |
| --- | --- | --- | --- |
| Job | `101` | Broken air conditioner | unassigned |
| Job | `102` | Leaking pipe | unassigned |
| Technician | `201` | alex@fieldco.com | AVAILABLE |
| Technician | `202` | sam@fieldco.com | ON_LEAVE |

Generate a signed local **manager token**:

```bash
uv run python -m scripts.make_demo_token --role manager --email manager@fieldco.com
```

Copy the printed token and pass it as the `Authorization` header. In Swagger UI, expand a `/demo` endpoint, click **Try it out**, and enter `Bearer <token>` in the authorization header field. Or use curl:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:8000/demo/jobs
```

Make a technician token with `--role technician --email alex@fieldco.com`. `/demo/technicians` returns 403 for technicians.

Token generation and validation use the same local key (set `LAB_JWT_SECRET` in your environment to override the demo fallback). For class exercises, use only fake identities and data. Never expose the demo default key on a deployed service.

## 4. Learning Plan

| Phase | Expected output | Suggested time |
| --- | --- | --- |
| Activity 1: Requirements | Refined FR/NFR, quality audit, stories, Gherkin | 35 min |
| Activity 2: Design | Use case, class and sequence diagrams (Mermaid), critique | 35 min |
| Activity 3: Coding | Assign Job in four layers, passing tests, review notes | 45 min |
| Wrap-up | Compare assumptions and explain risks | 5 min |

The original source estimates approximately 45 minutes for each activity; the timing above is an adjusted two-hour classroom plan.

**Start here:** read `LAB_WORKSHEET.md` and `specs/business_brief.md`. Do not jump directly to Activity 3: reuse your own requirements and diagrams as context for AI-assisted coding.

## 5. Coding Task: Build Assign Job

Read **`spec_assign_job.md`**. Ask your AI agent to implement the feature, with these new files:

```text
src/domain/repair_job.py
src/repository/job_repository.py
src/service/job_service.py
src/api/job_router.py
```

You may add repository adapter files as needed. Wire the router into `create_app()` in `src/main.py`. The existing `SeedStore` in `src/repository/seed_store.py` is intentionally supplied as a simple persistence boundary; **do not implement a second disconnected database**. Inject the store and services through FastAPI dependencies. Keep auth validation in the API layer using `src/api/auth.py`.

Expected endpoint:

```http
POST /jobs/{job_id}/assign
Authorization: Bearer <manager-demo-token>
Content-Type: application/json

{"assignee_email": "alex@fieldco.com"}
```

Expected response for seeded job `00000000-0000-0000-0000-000000000101`:

```json
{"job_id": "00000000-0000-0000-0000-000000000101", "assignee_email": "alex@fieldco.com", "status": "assigned"}
```

Contract tests encode the main scenarios and error statuses. There is one deliberate FastAPI trap: FastAPI defaults to **422** for validation failures, whereas the lab specification requires **400**. Adapt the error handling for this endpoint without changing the contract tests.

## 6. Run Tests

Before implementation, verify your environment with:

```bash
uv run pytest tests/test_starter.py -q
```

After Activity 3, run:

```bash
uv run pytest tests/test_assign_contract.py -q
uv run pytest -q
uv run pytest --cov=src --cov-report=term-missing
```

**Expected progression:** starter tests green → contract tests red (404, endpoint missing) → contract tests green after implementation. Do not edit tests just to force green results. Add an independent notification test; the given contract tests do not verify asynchronous behavior.

## 7. Repository Map

```text
README.md                 setup and student guidance
LAB_WORKSHEET.md          learning activities and deliverables
specs/business_brief.md   raw scenario and stakeholder answers
spec_assign_job.md        feature specification for coding phase
src/main.py               FastAPI application factory
src/api/auth.py           simplified demo-signed JWT auth
src/api/demo_router.py    existing read-only endpoints
src/api/dependencies.py   per-app dependency injection
src/repository/seed_store.py  per-app seed data, reset on new app
src/domain/seed_models.py read-only starter models
tests/test_starter.py      baseline tests, should pass immediately
tests/test_assign_contract.py  feature tests, red before coding
```

## 8. Common Issues

- **`uv` command not found:** install uv and reopen the terminal.
- **Unexpected Python version:** run `uv python install 3.12`, then `uv sync --python 3.12`.
- **`401` on demo routes:** include `Authorization: Bearer <token>`; use `scripts.make_demo_token`.
- **`403` on `/demo/technicians`:** use a manager role, not a technician token.
- **`404` on `/jobs/{id}/assign`:** expected until you implement and mount the router.
- **`422` instead of `400`:** FastAPI's default validation behavior; follow the spec.
- **Lost changes after server restart:** intentional in-memory storage; restart resets seeded state.
- **Tests pass locally but differ in Swagger:** each `create_app()` in tests gets a fresh store; the server owns another store.
- **Offline sync / PostgreSQL / mobile UI not found:** they are intentionally out of scope for the runnable starter; include them in requirements and diagrams where appropriate.
