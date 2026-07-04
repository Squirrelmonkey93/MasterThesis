import geopandas as gpd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

from config import NL_boundary, grid
from searching import site_type, find_material
from combining_data import Sites, Finds

keramiek = find_material('keramiek')
rural = site_type('rural settlement')

def calculate_hexagon_density(data_set: DataFrame, export=False):
    hexagons = gpd.read_file(grid)
    # hexagons = hexagons.drop(['left', 'right', 'top', 'bottom', 'row_index', 'col_index'], axis=1)
    hexagons['sqkm'] = hexagons.area / 10 ** 6  # /10**6 for sqkm instead of sqm

    hexa_sites = gpd.sjoin(left_df=hexagons, right_df=data_set, how='left') #Left or polygons with zero points are discarded
    hexa_site_count = hexa_sites.groupby('id')['SiteID'].count().rename('Sitecount').reset_index()

    hexagons.sort_values(by=['id'])
    hexagons2 = hexagons.merge(hexa_site_count, on='id')
    hexagons2['density'] = hexagons2['Sitecount']/hexagons2['sqkm']
    hexagons2.loc[hexagons2['density'] == 0, 'density'] = np.nan
    if export:
        hexagons2.to_file('created_gpkgs/Hexagon_density.gpkg', driver='GPKG', layer='name')
    return hexagons2

def plot_hexagon_density(data_set: DataFrame, export=False):
    NL = gpd.read_file(NL_boundary)
    blegh = calculate_hexagon_density(data_set)
    ax = NL.boundary.plot(color='black')
    ax.set_axis_off()
    blegh.plot(column='density', cmap="viridis_r",ax=ax, legend=True, legend_kwds={'label':'Density'})
    plt.show()

plot_hexagon_density(Finds)
plot_hexagon_density(Sites)

def versus_plot(f_material: DataFrame, s_type: DataFrame):
    den_ker = calculate_hexagon_density(f_material)
    den_rur = calculate_hexagon_density(s_type)
    samen = den_ker.merge(den_rur, on=['id','left', 'right', 'top', 'bottom', 'row_index', 'col_index','geometry','sqkm'])
    # print(samen.head())
    samen.plot(kind='scatter', x='density_x', y='density_y')
    plt.xlabel("Site density")
    plt.ylabel("Find density")
    plt.show()

versus_plot(keramiek, rural)
