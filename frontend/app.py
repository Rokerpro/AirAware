"""Development-only Gradio shell for the AirAware forecast contract."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

import gradio as gr


DISCLAIMER = "Prototype, not health advice."
MOCK_STATIONS = [
    {"station_id": "mock_lagankhel", "station_name": "Lagankhel (mock)"},
    {"station_id": "mock_shantichowk", "station_name": "Shantichowk (mock)"},
    {"station_id": "mock_kias", "station_name": "KIAS (mock)"},
    {"station_id": "mock_gaushala", "station_name": "Gaushala (mock)"},
]


def get_stations() -> dict[str, list[dict[str, str]]]:
    """Return temporary development stations until the ML split is finalized."""

    return {"stations": MOCK_STATIONS}


def _validate_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("Date must use YYYY-MM-DD format.") from exc


def mock_forecast(
    station_id: str,
    today: str,
    language: str,
) -> dict[str, Any]:
    """Return the contract shape using development-only placeholder values."""

    station = next(
        (item for item in MOCK_STATIONS if item["station_id"] == station_id),
        None,
    )
    if station is None:
        raise ValueError("Choose a development station.")
    if language not in {"en", "ne"}:
        raise ValueError("Language must be en or ne.")

    forecast_for = _validate_date(today) + timedelta(days=1)
    if language == "ne":
        precaution = (
            "\u092d\u094b\u0932\u093f \u092c\u093e\u0939\u093f\u0930\u0940 "
            "PE/assembly \u0938\u0940\u092e\u093f\u0924 \u0917\u0930\u094d\u0928\u0947 "
            "\u0935\u093f\u091a\u093e\u0930 \u0917\u0930\u094d\u0928\u0941\u0939\u094b\u0938\u0964"
        )
        disclaimer = (
            "\u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a, "
            "\u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0938\u0932\u094d\u0932\u093e\u0939 "
            "\u0939\u094b\u0907\u0928\u0964"
        )
    else:
        precaution = (
            "Consider limiting outdoor PE or assembly tomorrow "
            "if the school risk policy requires it."
        )
        disclaimer = DISCLAIMER

    predicted_pm25 = 42.0
    return {
        "station_id": station_id,
        "station_name": station["station_name"],
        "forecast_for": forecast_for.isoformat(),
        "predicted_pm25": predicted_pm25,
        "aqi_band": "Unhealthy for Sensitive Groups",
        "warning": predicted_pm25 > 35,
        "baselines": {
            "persistence_pm25": 39.0,
            "cams_pm25": None,
        },
        "precaution": precaution,
        "disclaimer": disclaimer,
        "model_version": "mock_development_only",
    }


def forecast_for_ui(
    station_id: str,
    today: str,
    language: str,
) -> tuple[dict[str, Any] | None, str]:
    """Return a contract response or a clear validation error."""

    try:
        result = mock_forecast(station_id, today, language)
    except ValueError as exc:
        return None, f"Error: {exc}"
    return result, "Development mock only; not a real forecast."


def build_app() -> gr.Blocks:
    """Build the development demo shell."""

    station_choices = [
        (item["station_name"], item["station_id"])
        for item in get_stations()["stations"]
    ]

    with gr.Blocks(title="AirAware") as app:
        gr.Markdown(
            "# AirAware\n"
            "Kathmandu next-day PM2.5 forecast shell.\n\n"
            "**Development UI:** results are temporary mock values."
        )

        with gr.Row():
            station = gr.Dropdown(
                choices=station_choices,
                label="Monitoring station",
                value=station_choices[0][1] if station_choices else None,
            )
            today = gr.Textbox(
                label="Today (YYYY-MM-DD)",
                value=date.today().isoformat(),
            )
            language = gr.Radio(
                choices=["en", "ne"],
                label="Language",
                value="en",
            )

        forecast_button = gr.Button("Forecast tomorrow", variant="primary")
        result = gr.JSON(label="Forecast response")
        status = gr.Markdown()

        forecast_button.click(
            fn=forecast_for_ui,
            inputs=[station, today, language],
            outputs=[result, status],
        )

        gr.Markdown(
            f"**{DISCLAIMER}**\n\n"
            "Final station choices and model outputs will be connected after "
            "the time split and inference artifacts are ready."
        )

    return app


if __name__ == "__main__":
    build_app().launch()
