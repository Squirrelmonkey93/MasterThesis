import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from numpy.f2py.f2py2e import outmess
from scipy.stats import alpha

from combining_data import Sitesg


def create_buffer(infected, buffer_size=1000, print_stuff=False):
    infected["buffer"] = infected['geometry'].buffer(buffer_size)
    infected.set_geometry('buffer', inplace=True)
    if print_stuff:
        print('testI-1 \n', infected, '\n')
    return infected

def in_buffer(row, infected):
    point = row['geometry']
    return infected.contains(point).any()

def infect(uninfected, infected, print_stuff=False):
    uninfected['in_buffer'] = uninfected.apply(in_buffer, axis=1, args=(infected,))
    newly_infected = uninfected.loc[uninfected['in_buffer'] == True]
    uninfected.drop(newly_infected.index, inplace=True)

    if print_stuff:
        print('newlyI \n', newly_infected, '\n')

    infected = pd.concat([infected, newly_infected], ignore_index=True)

    if print_stuff:
        print('testI-2 \n', infected, '\n', infected.columns, '\n')
    return len(newly_infected), infected



# Buffer size range (1,5) gives buffer sizes of 1, 2, 3, and 4 km
buffer_size = 5000
    # [x * 1000 for x in range(15,17)]
S_id = '502' #fectio
def search_radius(Site_id, range_size, visualize=False):
    Sitesg['buffered'] = Sitesg['geometry'].buffer(range_size)
    location = Sitesg.loc[Sitesg['SiteID'] == Site_id]
    search_range = location.buffered.iloc[0]
    inside_range = Sitesg.loc[Sitesg['geometry'].within(search_range)]
    # print(location)
    if visualize:
        # Boundary of the Netherlands in 2025, provided by CBS
        NL = gpd.read_file("gpkgs/NL_Provincien_CBS2025.gpkg")
        # Plot boundary
        ax = NL.boundary.plot(color='black')
        location.buffered.plot(ax=ax, color='green', alpha=0.3)
        inside_range.plot(ax=ax, color='magenta')
        location.geometry.plot(ax=ax, color='blue')
        plt.show()
    return inside_range

# search_radius(Site_id=S_id, range_size=buffer_size, visualize=True)

outside_cluster = Sitesg.copy()
inside_cluster = gpd.GeoDataFrame()

# Start site and buffer
outside_cluster['buffered'] = outside_cluster['geometry'].buffer(buffer_size)
start_location = outside_cluster.loc[outside_cluster['SiteID'] == S_id]
inside_cluster = pd.concat([inside_cluster,start_location], ignore_index=True)

# Removing start site from starting df to prevent duplicates
outside_cluster = pd.merge(outside_cluster, inside_cluster, on=['SiteID','Site_CID','Name', 'Site_type', 'X','Y', 'geometry', 'buffered'], how='outer', indicator=True)
outside_cluster = outside_cluster.query("_merge == 'left_only'")
outside_cluster = outside_cluster.drop('_merge', axis=1)
outside_cluster = outside_cluster.reset_index(drop=True)

s = inside_cluster['buffered']
union = s.union_all()
print(inside_cluster)
print(union)
inside = outside_cluster.loc[outside_cluster['geometry'].within(union)]
if len(inside) > 1:
    inside_cluster = pd.concat([inside_cluster, inside], ignore_index=True)
    s = inside_cluster['buffered']
    union = s.union_all()

# Boundary of the Netherlands in 2025, provided by CBS
# NL = gpd.read_file("gpkgs/NL_Provincien_CBS2025.gpkg")

# Plot boundary
# ax = NL.boundary.plot(color='black')
# plt.show()

# print(union)