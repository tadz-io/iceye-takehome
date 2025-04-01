"""Project pipelines."""
from __future__ import annotations

from kedro.pipeline import Pipeline

from flood_alert.pipelines.pipeline import evaluate_flood_alert, set_flood_threshold


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = {
        "evaluate_flood_alert": evaluate_flood_alert,
        "__default__": set_flood_threshold,
    }
    return pipelines
