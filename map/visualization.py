import geopandas
import numpy as np
from sklearn import neighbors


def plot_points(df,figsize=(15,15)):
    gdf = geopandas.GeoDataFrame(df,geometry=geopandas.points_from_xy(df.lat, df.lat))
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world.boundary.plot(color='k',figsize=figsize)
    gdf.plot(ax=ax,column='class',legend=True)

