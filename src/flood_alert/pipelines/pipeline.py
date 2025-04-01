from kedro.pipeline import node, pipeline

from flood_alert.pipelines import nodes

set_flood_threshold = pipeline(
    [
        node(
            func=nodes.set_flood_threshold,
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

evaluate_flood_alert = pipeline(
    [
        node(
            func=nodes.merge_station_data,
            inputs={
                "stations_meta_data": "stations_meta_data",
                "gauge_measurements": "gauge_measurements"
            },
            outputs="station_gauge_measurements"
        ),
        node(
            func=nodes.flood_at_station,
            inputs={
                "data": "station_gauge_measurements",
                "threshold": "flood_threshold",
            },
            outputs="flood_at_station"
        ),
        node(
            func=nodes.flood_in_aoi,
            inputs={
                "aoi": "aois",
                "flood_alert": "flood_at_station",
            },
            outputs="flood_in_aoi"
        )
    ]
)
