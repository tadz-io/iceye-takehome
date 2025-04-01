import geopandas as gpd
from kedro.io import AbstractDataSet


class GeoPackageDataSet(AbstractDataSet):
    def __init__(self, filepath: str, layer: str = None):
        self.filepath = filepath
        self.layer = layer

    def _load(self) -> gpd.GeoDataFrame:
        return gpd.read_file(self.filepath, layer=self.layer)

    def _save(self, data: gpd.GeoDataFrame) -> None:
        data.to_file(self.filepath, layer=self.layer, driver="GPKG")

    def _describe(self) -> dict:
        return {"filepath": self.filepath, "layer": self.layer}
