import geopandas as gpd
import pandas as pd
from kedro.io import AbstractDataset


class GeoPackageDataSet(AbstractDataset):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _load(self) -> gpd.GeoDataFrame:
        gdf = gpd.read_file(self.filepath)
        if 'datetime' in gdf.columns:
            gdf['datetime'] = pd.to_datetime(gdf['datetime'])
        return gdf

    def _save(self, data: gpd.GeoDataFrame) -> None:
        data.to_file(self.filepath, driver="GPKG")

    def _describe(self) -> dict:
        return {"filepath": self.filepath}
