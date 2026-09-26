from __future__ import annotations

from datetime import date, timedelta
import random


def sample_feed(start: str, end: str) -> dict:
    """Deterministic synthetic data for UI testing only."""
    random.seed(42)
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    days = max(1, min((e - s).days + 1, 30))
    out = {"near_earth_objects": {}}

    for i in range(days):
        d = s + timedelta(days=i)
        objects = []
        for j in range(8):
            oid = str(900000 + i * 10 + j)
            dmin = 0.005 + random.random() * 1.2
            dmax = dmin * (1.3 + random.random() * 1.7)
            velocity = 4 + random.random() * 34
            miss = 40_000 + random.random() * 18_000_000

            objects.append(
                {
                    "id": oid,
                    "name": f"({oid}) AstroRisk Demo",
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": dmin,
                            "estimated_diameter_max": dmax,
                        }
                    },
                    "close_approach_data": [
                        {
                            "relative_velocity": {
                                "kilometers_per_second": str(velocity)
                            },
                            "miss_distance": {"kilometers": str(miss)},
                        }
                    ],
                    "absolute_magnitude_h": 20 + random.random() * 8,
                    "is_potentially_hazardous_asteroid": dmax > 0.5 and miss < 3_000_000,
                    "is_sentry_object": False,
                    "nasa_jpl_url": None,
                }
            )
        out["near_earth_objects"][d.isoformat()] = objects

    return out
