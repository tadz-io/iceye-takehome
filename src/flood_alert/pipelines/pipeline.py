from kedro.pipeline import node, pipeline

from .nodes import set_flood_threshold

set_flood_threshold = pipeline(
    [
        node(
            func=set_flood_threshold,
            inputs={
                "data": "gauge_measurements",
                "start_date": "params:base_line.start_date",
                "end_date": "params:base_line.end_date",
                "sigma": "params:base_line.sigma"
            },
            outputs="flood_threshold"
        )
    ]
)
