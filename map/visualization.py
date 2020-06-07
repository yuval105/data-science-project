import geopandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors
from matplotlib import cm
from matplotlib import colors
import pandas as pd

def plot_points(df,figsize=(15,15)):
    gdf = geopandas.GeoDataFrame(df,geometry=geopandas.points_from_xy(df.lat, df.lat))
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    ax = world.boundary.plot(color='k',figsize=figsize)
    gdf.plot(ax=ax,column='class',legend=True)

def knn_plot(df,k,figsize = (15,15)):
    data = df[['lat','lng']].to_numpy()
    classes,idx_to_class = pd.factorize(df['class'])
    x = np.arange(-180,180,1)
    y = np.arange(-90,90,1)
    clf = neighbors.KNeighborsClassifier(k,metric='haversine') # Use the haversine metric for real distance
    clf.fit(data*np.pi/180, classes) # Fit on radians and not on degrees
    xx,yy = np.meshgrid(x,y)
    pred = clf.predict(np.c_[xx.ravel(),yy.ravel()]*np.pi/180).reshape(xx.shape)
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world = world[['continent', 'geometry']]
    fig,ax = plt.subplots(figsize=figsize)
    gdf = geopandas.GeoDataFrame(df,geometry=geopandas.points_from_xy(df.lat, df.lat))
    cmap = cm.get_cmap('tab20')
    cmap = colors.ListedColormap(cmap.colors[:len(idx_to_class)])
    ax.pcolormesh(xx,yy,pred,cmap=cmap)
    world.boundary.plot(color='k',ax=ax)
    for i,c in enumerate(idx_to_class):
        gdf[gdf['class']==c].geometry.plot(ax=ax,color=cmap.colors[i],label=c)
    ax.legend()