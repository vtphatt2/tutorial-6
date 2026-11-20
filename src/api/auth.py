"""Minimal signed JWT authentication for local exercises (HS256, no external auth server).

Training-only security: no expiry/issuer/audience verification, key rotation, or user directory.
Do not deploy this demo authentication to production.
"""
import base64
import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from fastapi import Depends, Header, HTTPException

DEFAULT_DEMO_SECRET = "tutorial-6-local-only-change-me"


@dataclass(frozen=True, slots=True)
class Actor:
    email: str
    role: str


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def _secret() -> bytes:
    return os.environ.get("LAB_JWT_SECRET", DEFAULT_DEMO_SECRET).encode()


def create_demo_token(email: str, role: str) -> str:
    """Convenience for local demonstration/testing, not a login service."""
    header = _b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = _b64encode(json.dumps({"sub": email, "role": role}).encode())
    signing_input = f"{header}.{payload}".encode()
    signature = _b64encode(hmac.new(_secret(), signing_input, hashlib.sha256).digest())
    return f"{header}.{payload}.{signature}"


def get_current_actor(authorization: str | None = Header(default=None)) -> Actor:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    try:
        token = authorization.removeprefix("Bearer ")
        header, payload, signature = token.split(".")
        header_data = json.loads(_b64decode(header))
        if header_data.get("alg") != "HS256":
            raise ValueError("Unsupported algorithm")
        expected = hmac.new(_secret(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, _b64decode(signature)):
            raise ValueError("Bad signature")
        data = json.loads(_b64decode(payload))
        if not isinstance(data.get("sub"), str) or data.get("role") not in ("manager", "technician"):
            raise ValueError("Invalid claims")
        return Actor(email=data["sub"], role=data["role"])
    except (ValueError, TypeError, KeyError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
