"""Script for plotting on a map of the NLs"""
import geopandas as gpd
import matplotlib.pyplot as plt

from searching import site_name, site_id, site_type, find_material, find_type

# Functions for specifics
Name = site_name('Hallum-Dorp')
ID = site_id('7680')
SType = site_type('rural settlement')
Material = find_material('textiel')
FType = find_type('amfibie')

# Boundary of the Netherlands in 2025, provided by CBS
NL = gpd.read_file("gpkgs/NL_Provincien_CBS2025.gpkg")

# Plot boundary
ax = NL.boundary.plot(color='black')

# Plot for the specifics, comment out what is not needed.
Name.plot(ax=ax, color='magenta')
ID.plot(ax=ax, color='red')
SType.plot(ax=ax, color='green')
Material.plot(ax=ax, color='cyan')
FType.plot(ax=ax, color='blue')

plt.show()