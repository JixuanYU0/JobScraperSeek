"""Optional authentication middleware for API security."""

import os
from typing import Optional
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

# Load API keys from environment
API_KEYS = os.getenv("API_KEYS", "").split(",")
API_KEYS = [key.strip() for key in API_KEYS if key.strip()]

# If no API keys configured, authentication is disabled
AUTH_ENABLED = len(API_KEYS) > 0

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    Verify API key from request header.

    Usage in endpoints:
        @app.get("/protected-endpoint")
        async def protected_route(api_key: str = Depends(verify_api_key)):
            # This endpoint requires valid API key
            pass

    To enable authentication:
        1. Add API_KEYS to .env file:
           API_KEYS=your-secret-key-1,your-secret-key-2

        2. Add dependency to endpoints:
           @app.get("/api/v1/scrape", dependencies=[Depends(verify_api_key)])

        3. Clients must include header:
           X-API-Key: your-secret-key-1
    """
    if not AUTH_ENABLED:
        # Authentication disabled - allow all requests
        return "auth_disabled"

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return api_key


def generate_api_key() -> str:
    """
    Generate a secure random API key.

    Usage:
        python -c "from src.api.auth import generate_api_key; print(generate_api_key())"
    """
    import secrets
    return secrets.token_urlsafe(32)


if __name__ == "__main__":
    # Script to generate API keys
    print("Generated API Key:")
    print(generate_api_key())
    print("\nAdd this to your .env file:")
    print(f"API_KEYS={generate_api_key()}")
