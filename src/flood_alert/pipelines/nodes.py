import geopandas as gpd
import pandas as pd


def set_flood_threshold(
        data: pd.DataFrame,
        start_date: str,
        end_date: str,
        sigma: int = 1) -> pd.DataFrame:
    """
    Set threshold for flood warning.

    Args:
        data (pd.DataFrame): _description_
        sigma (int): _description_

    Returns:
        pd.DataFrame: _description_
    """
    data_range = slice(pd.to_datetime(start_date), pd.to_datetime(end_date))
    # filter to dates between start_date and end_date to set baseline
    filtered_data = data.sort_index().loc[:, data_range, :]
    # calculate mean and standard deviation of absolute water levels
    data_stats = filtered_data.groupby('station_id')[
        'absolute_water_level_meters'
    ].agg(['mean', 'std'])
    # add threshold
    data_stats['threshold'] = data_stats['mean'] + sigma * data_stats['std']

    return data_stats['threshold']


def merge_station_data(
        stations_meta_data: gpd.GeoDataFrame,
        gauge_measurements: pd.DataFrame,
        ) -> gpd.GeoDataFrame:
    """_summary_

    Args:
        aoi (gpd.GeoDataFrame): _description_
        flood_data (pd.Series): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """

    # merge station meta data and gauge measurements
    return stations_meta_data.merge(gauge_measurements, how='left', on='station_id')


def flood_at_station(data: gpd.GeoDataFrame, threshold: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Args:
        data (pd.DataFrame): _description_
        threshold (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    flood_at_station = pd.merge(data, threshold, how='left', on='station_id')

    flood_at_station['flood_alert'] = flood_at_station.apply(
        lambda x: x.absolute_water_level_meters > x.threshold, axis=1)

    return flood_at_station


def flood_in_aoi(aoi: gpd.GeoDataFrame, flood_alert: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """_summary_

    Args:
        aoi (gpd.GeoDataFrame): _description_
        flood_alert (gpd.GeoDataFrame): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    # spatial join of aoi and flood alert data
    flood_in_aoi = aoi.sjoin(flood_alert, how='left')

    # return aoi where flood alert has been triggered
    return flood_in_aoi.where(flood_in_aoi['flood_alert']).dropna()
