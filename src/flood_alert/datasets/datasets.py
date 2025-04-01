import geopandas as gpd
import pandas as pd
from kedro.io import AbstractDataset


class GeoPackageDataSet(AbstractDataset):
    def __init__(self, filepath: str, index: str):
        self.filepath = filepath
        self.index = index

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
        data.to_file(self.filepath, driver="GPKG")

    def _describe(self) -> dict:
        return {"filepath": self.filepath}
