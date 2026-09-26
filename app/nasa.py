from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.nasa.gov/neo/rest/v1"
CACHE = Path(__file__).resolve().parent.parent / "data" / "neo_cache.json"
TTL = int(os.getenv("ASTRORISK_CACHE_MINUTES", "30")) * 60


class NASAError(RuntimeError):
    pass


async def _get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    params = dict(params or {})
    params["api_key"] = os.getenv("NASA_API_KEY", "DEMO_KEY")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{BASE}{path}", params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:500]
        raise NASAError(f"NASA NeoWs returned HTTP {exc.response.status_code}: {detail}") from exc
    except httpx.HTTPError as exc:
        raise NASAError(f"Could not reach NASA NeoWs: {exc}") from exc


def _load_cache() -> dict[str, Any] | None:
    if not CACHE.exists():
        return None
    try:
        data = json.loads(CACHE.read_text(encoding="utf-8"))
        if time.time() - float(data["timestamp"]) < TTL:
            return data["payload"]
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None
    return None


def _save_cache(payload: dict[str, Any]) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(
        json.dumps({"timestamp": time.time(), "payload": payload}),
        encoding="utf-8",
    )


async def feed(start_date: str, end_date: str, force: bool = False) -> dict[str, Any]:
    # The cache is only safe to reuse for identical requests.
    if not force and CACHE.exists():
        try:
            cached = json.loads(CACHE.read_text(encoding="utf-8"))
            if (
                cached.get("start_date") == start_date
                and cached.get("end_date") == end_date
                and time.time() - float(cached["timestamp"]) < TTL
            ):
                return cached["payload"]
        except Exception:
            pass

    payload = await _get("/feed", {"start_date": start_date, "end_date": end_date})
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(
        json.dumps(
            {
                "timestamp": time.time(),
                "start_date": start_date,
                "end_date": end_date,
                "payload": payload,
            }
        ),
        encoding="utf-8",
    )
    return payload


async def asteroid(asteroid_id: str) -> dict[str, Any]:
    return await _get(f"/neo/{asteroid_id}")


async def browse(page: int = 0, size: int = 20) -> dict[str, Any]:
    return await _get("/neo/browse", {"page": page, "size": size})
