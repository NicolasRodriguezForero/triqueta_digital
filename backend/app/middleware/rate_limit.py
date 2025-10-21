"""
Simple rate limiting dependency using Redis and fixed window counters.
"""
from __future__ import annotations
from typing import Callable, Tuple
from fastapi import HTTPException, Request, status

from app.utils.redis_client import get_redis


def _parse_rate(rate: str) -> Tuple[int, int]:
    """Parse rate string like '5/15minute', '10/minute', '100/hour'.
    Returns (max_requests, window_seconds).
    """
    try:
        # Split count and period
        count_part, period_part = rate.split("/")
        max_requests = int(count_part)

        # Normalize period
        period_part = period_part.strip().lower()
        # Accept forms like '15minute', '15minutes', 'minute', 'hour', 'second'
        num = ""
        unit = ""
        for ch in period_part:
            if ch.isdigit():
                num += ch
            else:
                unit += ch
        unit = unit or "minute"
        amount = int(num) if num else 1

        if unit.startswith("sec"):
            window = amount
        elif unit.startswith("min"):
            window = amount * 60
        elif unit.startswith("hour"):
            window = amount * 60 * 60
        elif unit.startswith("day"):
            window = amount * 24 * 60 * 60
        else:
            # default minute
            window = amount * 60
        return max_requests, window
    except Exception:
        # Fallback to 5 per 15 minutes
        return 5, 15 * 60


def rate_limit_ip(rate: str, scope: str) -> Callable[[Request], None]:
    """Factory for a FastAPI dependency that enforces a rate limit per IP per scope.

    Usage:
        Depends(rate_limit_ip(settings.RATE_LIMIT_LOGIN, scope="login"))
    """
    from app.core.config import settings
    
    max_requests, window = _parse_rate(rate)

    async def _dependency(request: Request) -> None:
        # Skip rate limiting if disabled (e.g., in tests)
        if not settings.RATE_LIMIT_ENABLED:
            return
        
        client_ip = request.client.host if request.client else "unknown"
        key = f"rl:{scope}:{client_ip}"
        r = get_redis()

        # INCR the counter and set TTL if first time
        current = await r.incr(key)
        if current == 1:
            await r.expire(key, window)

        if current > max_requests:
            ttl = await r.ttl(key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "message": "Too many requests. Please try again later.",
                    "retry_after": max(ttl, 0),
                },
            )

    return _dependency
