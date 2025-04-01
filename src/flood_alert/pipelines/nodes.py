from datetime import datetime

import pandas as pd


def set_flood_threshold(data: pd.DataFrame, start_date: str, end_date: str, sigma: int = 1) -> pd.DataFrame:
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
    data_stats = filtered_data.groupby('station_id')['absolute_water_level_meters'].agg(['mean', 'std'])
    # add threshold
    data_stats['threshold'] = data_stats['mean'] + sigma * data_stats['std']

    return data_stats['threshold']


def exceeds_flood_threshold(data: pd.DataFrame, threshold: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Args:
        data (pd.DataFrame): _description_
        threshold (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    merged_data = pd.merge(data, threshold, how='left', left_index=True, right_index=True)

    exceeds_threshold = merged_data.apply(lambda x: x.absolute_water_level_meters > x.threshold,
                                          axis=1)
    # set name of pd.Series
    exceeds_threshold.name = 'exceeds_threshold'

    return exceeds_threshold
