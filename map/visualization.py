import geopandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors
from matplotlib import cm
from matplotlib import colors
import pandas as pd
from IPython import display
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import GeoJSONDataSource, ColumnDataSource, Range1d
from bokeh.transform import factor_cmap
from bokeh.models.tools import HoverTool
import bokeh
from bokeh.resources import INLINE


def plot_points(df, figsize=(15, 15), column='class'):
    gdf = geopandas.GeoDataFrame(
        df.copy(), geometry=geopandas.points_from_xy(df.lng, df.lat))
    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world.boundary.plot(color='k', figsize=figsize)
    gdf.plot(ax=ax, column=column, legend=True)


def knn_plot(df, k, figsize=(15, 15), column='class'):
    data = df[['lng', 'lat']].to_numpy()
    classes, idx_to_class = pd.factorize(df[column])
    x = np.arange(-180, 180, 0.5)
    y = np.arange(-90, 90, 0.5)
    # Use the haversine metric for real distance
    clf = neighbors.KNeighborsClassifier(k, metric='haversine')
    clf.fit(data*np.pi/180, classes)  # Fit on radians and not on degrees
    xx, yy = np.meshgrid(x, y)
    pred = clf.predict(np.c_[xx.ravel(), yy.ravel()]
                       * np.pi/180).reshape(xx.shape)
    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres'))
    world = world[['continent', 'geometry']]
    fig, ax = plt.subplots(figsize=figsize)
    gdf = geopandas.GeoDataFrame(
        df.copy(), geometry=geopandas.points_from_xy(df.lng, df.lat))
    cmap = cm.get_cmap('tab20', len(idx_to_class))
    ax.pcolormesh(xx, yy, pred, cmap=cmap)
    world.boundary.plot(color='k', ax=ax)
    for i, c in enumerate(idx_to_class):
        gdf[gdf[column] == c].geometry.plot(
            ax=ax, color=cmap.colors[i], label=c)
    ax.legend()


def plot_interactive_points(df, column='class'):
    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres'))
    world_source = GeoJSONDataSource(geojson=world.to_json())
    points_source = ColumnDataSource(df)
    _, classes = pd.factorize(df[column])
    cmap = cm.get_cmap('tab20', len(classes))
    colors = list(map(lambda x: bokeh.colors.RGB(
        x[0]*255, x[1]*255, x[2]*255, x[3]), cmap.colors))
    color_tranform = factor_cmap(column, palette=colors, factors=classes)
    p = figure(tools=['pan', 'wheel_zoom'],active_scroll='wheel_zoom', plot_width=800, plot_height=400)
    p.multi_line('xs', 'ys', source=world_source, color='black', line_width=3)
    circles = p.circle('lng', 'lat', size=8, color=color_tranform,
                       source=points_source, legend_group=column)
    p.add_tools(
        HoverTool(tooltips=[("Architecture", f"@{column}")], renderers=[circles]))
    output_notebook(INLINE)
    show(p)
