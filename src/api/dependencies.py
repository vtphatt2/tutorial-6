"""Inversion-of-control boundary used by routers, not global mutable state."""
from fastapi import Request
from src.repository.seed_store import SeedStore


def get_seed_store(request: Request) -> SeedStore:
    return request.app.state.seed_store
