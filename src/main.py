from fastapi import FastAPI
from src.api.demo_router import router as demo_router
from src.repository.seed_store import SeedStore


def create_app() -> FastAPI:
    app = FastAPI(title="Field Repair Tracker - Tutorial 6 Lab")
    app.state.seed_store = SeedStore()
    app.include_router(demo_router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    # STUDENT TODO (Activity 3): include your assign-job router here.
    return app


app = create_app()
