import secrets
from typing import Optional


def generate_state_token() -> str:
    return secrets.token_urlsafe(32)


def verify_state_token(token: str, expected: str) -> bool:
    return secrets.compare_digest(token, expected)


def hash_token(token: str) -> str:
    return secrets.token_hex(16)
