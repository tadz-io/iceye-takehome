import geopandas as gpd
import pandas as pd


def set_flood_threshold(
    data: pd.DataFrame, start_date: str, end_date: str, sigma: int = 1
) -> pd.DataFrame:
    """
    Set threshold for flood warning. Flood threshold is determined by taking
    the mean over all gauge measurements within [start_date, end_date] plus
    sigma * standard deviation.

    Args:
        data (pd.DataFrame): Dataframe containing the gauge measurements under column
            'absolute_water_level_meters' and station id's under column 'station_id'
        sigma (int): The number of standard deviation above the mean water level that constitutes
            a flood event

    Returns:
        pd.DataFrame: Dataframe containing the water level threshold for a flood event in meters
    """
    data_range = slice(pd.to_datetime(start_date), pd.to_datetime(end_date))
    # reset indices on dataframe
    data = data.reset_index().set_index(["station_id", "datetime"])
    # filter to dates between start_date and end_date to set baseline
    filtered_data = data.sort_index().loc[:, data_range, :]
    # calculate mean and standard deviation of absolute water levels
    data_stats = filtered_data.groupby("station_id")["absolute_water_level_meters"].agg(
        ["mean", "std"]
    )
    # add threshold
    data_stats["threshold"] = data_stats["mean"] + sigma * data_stats["std"]

    return data_stats["threshold"]


def merge_station_data(
    stations_meta_data: gpd.GeoDataFrame,
    gauge_measurements: pd.DataFrame,
) -> gpd.GeoDataFrame:
    """
    Merge station meta data with gauge measurements

    Args:
        stations_meta_data (gpd.GeoDataFrame): Meta data per station including geometries.
            Stations should have an identifier under column 'station_id'
        gauge_measurements (pd.DataFrame): Dataframe containing the gauge measurements per station

    Returns:
        gpd.GeoDataFrame: merged GeoDataFrame containing meta and gauge data per station
    """

    # merge station meta data and gauge measurements
    return stations_meta_data.merge(gauge_measurements, how="left", on="station_id")


def flood_at_station(
    data: gpd.GeoDataFrame, threshold: pd.DataFrame
) -> gpd.GeoDataFrame:
    """
    Determines if a flood alert was triggered per station per timestamp

    Args:
        data (pd.GeoDataFrame): Merged station meta data and gauge measurements including
            geolocation threshold (pd.DataFrame): Flood threshold per station as DataFrame

    Returns:
        gpd.GeoDataFrame: Dataframe with flood alert (`flood_alert`) as boolean per station,
          per time stamp and geolocation
    """
    flood_at_station = pd.merge(data, threshold, how="left", on="station_id")
    # check if gauge measurements exceeded flood threshold for every station at every timestamp
    flood_at_station["flood_alert"] = flood_at_station.apply(
        lambda x: x.absolute_water_level_meters > x.threshold, axis=1
    )

    return flood_at_station


def flood_in_aoi(
    aoi: gpd.GeoDataFrame, flood_alert: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Determines if a flood alert was triggered in an AOI. Only returns AOI for which a flood
        event happened.

    Args:
        aoi (gpd.GeoDataFrame): GeoDataFrame containing the AOIs and geometries delineating the area
        flood_alert (gpd.GeoDataFrame): Dataframe with flood alert per station per timestamp

    Returns:
        gpd.GeoDataFrame: GeoDataFrame of flooded AOIs
    """
    # spatial join of aoi and flood alert data
    flood_in_aoi = aoi.sjoin(flood_alert, how="left")

    # return aoi where flood alert has been triggered
    return flood_in_aoi.where(flood_in_aoi["flood_alert"]).dropna()
