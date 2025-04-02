from typing import Literal

import geopandas as gpd
import pandas as pd
from kedro.io import AbstractDataset


class GeoPackageDataSet(AbstractDataset):
    """
    A Kedro dataset for reading and writing geospatial data using GeoPandas.

    Args:
        filepath (str): Path to the GeoPackage or GeoJSON file.
        index (str, optional): Column to set as the index. Defaults to None.
        driver (Literal['GPKG', 'GeoJSON']): Format for saving the data. Defaults to 'GPKG'.

    Methods:
        _load() -> gpd.GeoDataFrame:
            Loads geospatial data, casts datetime columns, and sets the index if specified.
        _save(data: gpd.GeoDataFrame) -> None:
            Saves the GeoDataFrame to the specified file.
        _describe() -> dict:
            Returns a description of the dataset.
    """
    def __init__(
            self,
            filepath: str,
            index: str = None,
            driver: Literal['GPKG', 'GeoJSON'] = 'GPKG'):
        self.filepath = filepath
        self.index = index
        self.driver = driver

    def _load(self) -> gpd.GeoDataFrame:
        gdf = gpd.read_file(self.filepath)
        # cast datetime column (str) to datetime dtype
        if 'datetime' in gdf.columns:
            gdf['datetime'] = pd.to_datetime(gdf['datetime'])
        # set index for dataframe if specified
        if self.index is not None:
            gdf.set_index(self.index, inplace=True)
        return gdf

    def _save(self, data: gpd.GeoDataFrame) -> None:
        data.to_file(self.filepath, driver=self.driver)

    def _describe(self) -> dict:
        return {"filepath": self.filepath}
