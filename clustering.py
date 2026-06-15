import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

from config import NL_boundary
from combining_data import Sites

# Buffer size range (1,5) gives buffer sizes of 1, 2, 3, and 4 km
buffer_size = 5000
    # [x * 1000 for x in range(15,17)]
S_id = '502' #fectio
def search_radius(Site_id, range_size, visualize=False):
    Sites['buffered'] = Sites['geometry'].buffer(range_size)
    location = Sites.loc[Sites['SiteID'] == Site_id]
    search_range = location.buffered.iloc[0]
    inside_range = Sites.loc[Sites['geometry'].within(search_range)]
    # print(location)
    if visualize:
        # Boundary of the Netherlands in 2025, provided by CBS
        NL = gpd.read_file(NL_boundary)
        # Plot boundary
        ax = NL.boundary.plot(color='black')
        location.buffered.plot(ax=ax, color='magenta', alpha=0.3)
        inside_range.plot(ax=ax, color='green')
        location.geometry.plot(ax=ax, color='blue')
        plt.show()
    return inside_range

search_radius(Site_id=S_id, range_size=buffer_size, visualize=True)

def clustering(Site_id, range_size, visualize=False):
    outside_cluster = Sites.copy()
    inside_cluster = gpd.GeoDataFrame()

    # Start site and buffer
    outside_cluster['buffered'] = outside_cluster['geometry'].buffer(range_size)
    start_location = outside_cluster.loc[outside_cluster['SiteID'] == Site_id]
    inside_cluster = pd.concat([inside_cluster,start_location], ignore_index=True)

    # Removing start site from starting df to prevent duplicates
    outside_cluster = pd.merge(outside_cluster, inside_cluster, on=['SiteID','Site_CID','Name', 'Site_type', 'X','Y', 'geometry', 'buffered'], how='outer', indicator=True)
    outside_cluster = outside_cluster.query("_merge == 'left_only'")
    outside_cluster = outside_cluster.drop('_merge', axis=1)
    outside_cluster = outside_cluster.reset_index(drop=True)

    s = inside_cluster['buffered']
    union = s.union_all()
    # print(inside_cluster)
    # print(union)
    inside = outside_cluster.loc[outside_cluster['geometry'].within(union)]
    while len(inside) > 0:
        inside_cluster = pd.concat([inside_cluster, inside], ignore_index=True)
        s = inside_cluster['buffered']
        union = s.union_all()
        inside = outside_cluster.loc[outside_cluster['geometry'].within(union)]

        # Removing start site from starting df to prevent duplicates
        outside_cluster = pd.merge(outside_cluster, inside_cluster,
                                   on=['SiteID', 'Site_CID', 'Name', 'Site_type', 'X', 'Y', 'geometry', 'buffered'],
                                   how='outer', indicator=True)
        outside_cluster = outside_cluster.query("_merge == 'left_only'")
        outside_cluster = outside_cluster.drop('_merge', axis=1)
        outside_cluster = outside_cluster.reset_index(drop=True)

    if visualize:
        # Boundary of the Netherlands in 2025, provided by CBS
        NL = gpd.read_file(NL_boundary)
        # Plot boundary
        ax = NL.boundary.plot(color='black')
        inside_cluster.plot(ax=ax, color='green')
        start_location.geometry.plot(ax=ax, color='blue')
        plt.show()
    return inside_cluster

clustering(Site_id=S_id, range_size=buffer_size, visualize=True)