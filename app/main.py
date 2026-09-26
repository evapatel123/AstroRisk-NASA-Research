from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .analytics import cluster, filter_dataframe, observations_from_feed, summary
from .nasa import NASAError, asteroid as nasa_asteroid, browse as nasa_browse, feed as nasa_feed
from .sample_data import sample_feed

APP_ROOT = "app"

app = FastAPI(
    title="AstroRisk API",
    version="1.1.0",
    description=(
        "NASA NeoWs exploratory near-Earth asteroid analysis API. "
        "Developer: Eva J. Patel."
    ),
)

app.mount("/static", StaticFiles(directory=f"{APP_ROOT}/static"), name="static")


def default_dates() -> tuple[str, str]:
    end = date.today()
    start = end - timedelta(days=6)
    return start.isoformat(), end.isoformat()


async def get_dataframe(
    start: str,
    end: str,
    demo_fallback: bool = True,
) -> tuple[pd.DataFrame, str]:
    try:
        payload = await nasa_feed(start, end)
        df = observations_from_feed(payload)
        if not df.empty:
            return df, "NASA NeoWs"
    except NASAError:
        if not demo_fallback:
            raise

    if demo_fallback:
        return observations_from_feed(sample_feed(start, end)), "Demo fallback"

    raise HTTPException(status_code=502, detail="NASA NeoWs returned no usable observations.")


@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(f"{APP_ROOT}/static/index.html")


@app.get("/api/health")
async def health():
    return {
        "status": "online",
        "developer": "Eva J. Patel",
        "source": "NASA NeoWs",
        "research_lab": "/lab",
    }


@app.get("/api/feed")
async def api_feed(
    start: str | None = None,
    end: str | None = None,
    diameter_min: float | None = None,
    diameter_max: float | None = None,
    velocity_min: float | None = None,
    velocity_max: float | None = None,
    distance_min: float | None = None,
    distance_max: float | None = None,
):
    d0, d1 = default_dates()
    start = start or d0
    end = end or d1

    if start > end:
        raise HTTPException(status_code=400, detail="Start date must be before end date.")

    df, source = await get_dataframe(start, end)
    df = filter_dataframe(
        df,
        {
            "start": start,
            "end": end,
            "diameter_min": diameter_min,
            "diameter_max": diameter_max,
            "velocity_min": velocity_min,
            "velocity_max": velocity_max,
            "distance_min": distance_min,
            "distance_max": distance_max,
        },
    )

    clustered, model = cluster(df)

    return {
        "source": source,
        "summary": summary(df),
        "model": model,
        "rows": clustered.head(500).where(pd.notna(clustered.head(500)), None).to_dict(
            orient="records"
        ),
    }


@app.get("/api/asteroid/{asteroid_id}")
async def api_asteroid(asteroid_id: str):
    try:
        return await nasa_asteroid(asteroid_id)
    except NASAError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/browse")
async def api_browse(
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
):
    try:
        return await nasa_browse(page, size)
    except NASAError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


def build_gradio_app():
    # Matplotlib is declared in requirements.txt.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import gradio as gr

    async def run_lab(
        start,
        end,
        dmin,
        dmax,
        vmin,
        vmax,
        distmin,
        distmax,
        k,
    ):
        df, source = await get_dataframe(str(start), str(end))
        df = filter_dataframe(
            df,
            {
                "diameter_min": dmin,
                "diameter_max": dmax,
                "velocity_min": vmin,
                "velocity_max": vmax,
                "distance_min": distmin,
                "distance_max": distmax,
            },
        )

        clustered, model = cluster(df, int(k))
        stats = summary(df)
        stats["source"] = source

        fig1, ax1 = plt.subplots(figsize=(7, 4))
        if not df.empty:
            ax1.scatter(
                df["diameter_km"],
                df["velocity_km_s"],
                alpha=0.55,
                s=18,
            )
        ax1.set_xscale("log")
        ax1.set_xlabel("Diameter (km)")
        ax1.set_ylabel("Relative velocity (km/s)")
        ax1.set_title("Diameter vs Relative Velocity")
        ax1.grid(alpha=0.15)

        fig2, ax2 = plt.subplots(figsize=(7, 4))
        if not df.empty:
            ax2.scatter(
                df["miss_distance_km"],
                df["velocity_km_s"],
                alpha=0.55,
                s=18,
            )
        ax2.set_xscale("log")
        ax2.set_xlabel("Miss distance (km)")
        ax2.set_ylabel("Relative velocity (km/s)")
        ax2.set_title("Miss Distance vs Relative Velocity")
        ax2.grid(alpha=0.15)

        preview_columns = [
            "name",
            "date",
            "diameter_km",
            "velocity_km_s",
            "miss_distance_km",
            "is_potentially_hazardous",
            "category",
        ]
        preview = clustered[
            [c for c in preview_columns if c in clustered.columns]
        ].head(100)

        return stats, model, fig1, fig2, preview

    with gr.Blocks(
        title="AstroRisk Research Lab",
        theme=gr.themes.Base(),
    ) as demo:
        gr.Markdown(
            """
# AstroRisk Research Lab
### NASA NeoWs exploratory analysis
**Developer: Eva J. Patel**

This laboratory supports descriptive statistical analysis and exploratory
clustering. The model is **not** an impact-probability predictor.
"""
        )

        with gr.Row():
            start = gr.Textbox(label="Start date", value=default_dates()[0])
            end = gr.Textbox(label="End date", value=default_dates()[1])

        with gr.Row():
            dmin = gr.Number(label="Min diameter (km)", value=0)
            dmax = gr.Number(label="Max diameter (km)", value=100)
            vmin = gr.Number(label="Min velocity (km/s)", value=0)
            vmax = gr.Number(label="Max velocity (km/s)", value=100)

        with gr.Row():
            distmin = gr.Number(label="Min miss distance (km)", value=0)
            distmax = gr.Number(label="Max miss distance (km)", value=1_000_000_000)
            k = gr.Slider(label="Number of clusters (K)", minimum=2, maximum=5, step=1, value=3)

        run = gr.Button("RUN ANALYSIS", variant="primary")

        with gr.Row():
            stats = gr.JSON(label="Descriptive statistics")
            model = gr.JSON(label="Exploratory K-means model")

        with gr.Row():
            p1 = gr.Plot(label="Diameter × velocity")
            p2 = gr.Plot(label="Miss distance × velocity")

        table = gr.Dataframe(label="Filtered observations", interactive=False)

        run.click(
            run_lab,
            inputs=[start, end, dmin, dmax, vmin, vmax, distmin, distmax, k],
            outputs=[stats, model, p1, p2, table],
        )

    return demo


# IMPORTANT: mount Gradio after defining the FastAPI application.
# There is intentionally no silent try/except here: if Gradio cannot initialize,
# startup should show the actual error rather than producing a mysterious /lab 404.
try:
    import gradio as _gradio
except ImportError as exc:
    raise RuntimeError(
        "Gradio is missing. Run: python -m pip install -r requirements.txt"
    ) from exc

try:
    _demo = build_gradio_app()
    app = _gradio.mount_gradio_app(app, _demo, path="/lab")
    print("ASTRORISK: Gradio Research Lab mounted at /lab")
except Exception as exc:
    raise RuntimeError(
        f"AstroRisk could not initialize the Gradio Research Lab: {exc}"
    ) from exc
