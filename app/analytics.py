from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

FEATURES = ["diameter_km", "velocity_km_s", "miss_distance_km"]


def observations_from_feed(payload: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    for approach_date, objects in payload.get("near_earth_objects", {}).items():
        for obj in objects:
            diameter = obj.get("estimated_diameter", {}).get("kilometers", {})
            approaches = obj.get("close_approach_data") or []
            approach = approaches[0] if approaches else {}

            velocity_raw = (
                approach.get("relative_velocity", {})
                .get("kilometers_per_second")
            )
            miss_raw = approach.get("miss_distance", {}).get("kilometers")

            if velocity_raw is None or miss_raw is None:
                continue

            dmin = diameter.get("estimated_diameter_min")
            dmax = diameter.get("estimated_diameter_max")

            if dmin is None or dmax is None:
                continue

            rows.append(
                {
                    "id": str(obj.get("id", "")),
                    "name": str(obj.get("name", "")).replace("(", "").replace(")", ""),
                    "date": str(approach_date),
                    "diameter_min_km": float(dmin),
                    "diameter_max_km": float(dmax),
                    "diameter_km": (float(dmin) + float(dmax)) / 2,
                    "velocity_km_s": float(velocity_raw),
                    "miss_distance_km": float(miss_raw),
                    "absolute_magnitude_h": obj.get("absolute_magnitude_h"),
                    "is_potentially_hazardous": bool(
                        obj.get("is_potentially_hazardous_asteroid", False)
                    ),
                    "is_sentry_object": bool(obj.get("is_sentry_object", False)),
                    "nasa_jpl_url": obj.get("nasa_jpl_url"),
                }
            )

    return pd.DataFrame(rows)


def _corr(a: pd.Series, b: pd.Series, method: str) -> float | None:
    if len(a) < 3:
        return None
    value = a.corr(b, method=method)
    return None if pd.isna(value) else float(value)


def correlations(df: pd.DataFrame) -> dict[str, float | None]:
    pairs = [
        ("diameter_vs_velocity", "diameter_km", "velocity_km_s"),
        ("diameter_vs_miss_distance", "diameter_km", "miss_distance_km"),
        ("velocity_vs_miss_distance", "velocity_km_s", "miss_distance_km"),
    ]
    result: dict[str, float | None] = {}

    for label, a, b in pairs:
        result[f"{label}_pearson"] = _corr(df[a], df[b], "pearson")
        result[f"{label}_spearman"] = _corr(df[a], df[b], "spearman")

    return result


def summary(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {
            "count": 0,
            "unique_asteroids": 0,
            "hazardous_flagged": 0,
            "sentinel_objects": 0,
            "correlations": correlations_empty(),
        }

    return {
        "count": int(len(df)),
        "unique_asteroids": int(df["id"].nunique()),
        "hazardous_flagged": int(df["is_potentially_hazardous"].sum()),
        "sentinel_objects": int(df["is_sentry_object"].sum()),
        "diameter": numeric_summary(df["diameter_km"]),
        "velocity": numeric_summary(df["velocity_km_s"]),
        "miss_distance": numeric_summary(df["miss_distance_km"]),
        "correlations": correlations(df),
        "date_min": str(df["date"].min()),
        "date_max": str(df["date"].max()),
    }


def correlations_empty() -> dict[str, None]:
    names = [
        "diameter_vs_velocity",
        "diameter_vs_miss_distance",
        "velocity_vs_miss_distance",
    ]
    return {f"{n}_{m}": None for n in names for m in ("pearson", "spearman")}


def numeric_summary(series: pd.Series) -> dict[str, float]:
    return {
        "mean": float(series.mean()),
        "median": float(series.median()),
        "p10": float(series.quantile(0.10)),
        "p90": float(series.quantile(0.90)),
        "min": float(series.min()),
        "max": float(series.max()),
    }


def filter_dataframe(df: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
    out = df.copy()

    start = params.get("start")
    end = params.get("end")
    if start:
        out = out[out["date"] >= str(start)]
    if end:
        out = out[out["date"] <= str(end)]

    ranges = [
        ("diameter_km", "diameter_min", "diameter_max"),
        ("velocity_km_s", "velocity_min", "velocity_max"),
        ("miss_distance_km", "distance_min", "distance_max"),
    ]

    for col, low_key, high_key in ranges:
        low = params.get(low_key)
        high = params.get(high_key)
        if low is not None and float(low) >= 0:
            out = out[out[col] >= float(low)]
        if high is not None and float(high) >= 0:
            out = out[out[col] <= float(high)]

    return out


def cluster(df: pd.DataFrame, k: int = 3) -> tuple[pd.DataFrame, dict[str, Any]]:
    if len(df) < max(6, k):
        return df.copy(), {
            "available": False,
            "reason": "At least six complete observations are needed.",
        }

    work = df.copy()
    X = np.log1p(work[FEATURES].astype(float))
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=k, random_state=42, n_init=20)
    labels = model.fit_predict(X_scaled)
    work["cluster_id"] = labels

    centers = scaler.inverse_transform(model.cluster_centers_)
    centers = np.expm1(centers)
    center_df = pd.DataFrame(centers, columns=FEATURES)

    profile_score = (
        center_df["diameter_km"].rank(pct=True)
        + center_df["velocity_km_s"].rank(pct=True)
        + (1 - center_df["miss_distance_km"].rank(pct=True))
    )
    ordered = list(profile_score.sort_values().index)

    names: dict[int, str] = {}
    if ordered:
        names[ordered[0]] = "SMALL / SLOW / FAR"
        if len(ordered) >= 3:
            names[ordered[-1]] = "LARGE / FAST / CLOSE"
        for idx in ordered[1:-1]:
            names[idx] = "MIXED PROFILE"

    work["category"] = work["cluster_id"].map(names)

    return work, {
        "available": True,
        "k": k,
        "inertia": float(model.inertia_),
        "centroids": [
            {
                "cluster_id": int(i),
                "category": names.get(i, "MIXED PROFILE"),
                "diameter_km": float(row["diameter_km"]),
                "velocity_km_s": float(row["velocity_km_s"]),
                "miss_distance_km": float(row["miss_distance_km"]),
            }
            for i, row in center_df.iterrows()
        ],
    }
