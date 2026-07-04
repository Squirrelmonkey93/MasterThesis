"""Script for plotting on a map of the NLs"""
import geopandas as gpd
import matplotlib.pyplot as plt

from searching import site_name, site_id, site_type, find_material, find_type
from config import NL_boundary

def plotting(s_name:False, s_id:False, s_type:False, f_material:False, f_type:False):
    # Boundary of the Netherlands in 2025, provided by CBS
    NL = gpd.read_file(NL_boundary)

    # Plot boundary
    ax = NL.boundary.plot(color='black')
    ax.set_axis_off()

    # Plot for the specifics
    if s_name:
        site_name(s_name).plot(ax=ax, color='magenta', zorder=5, markersize=5)
    if s_id:
        site_id(s_id).plot(ax=ax, color='red', zorder=4, markersize=5)
    if s_type:
        site_type(s_type).plot(ax=ax, color='green', zorder=1, markersize=5)
    if f_material:
        find_material(f_material).plot(ax=ax, color='cyan', zorder=2, markersize=5)
    if f_type:
        find_type(f_type).plot(ax=ax, color='blue', zorder=3, markersize=5)

    plt.show()

Name = 'Hallum-Dorp'
ID = '502'
SType = 'rural settlement'
Material = 'textiel'
FType = 'amfibie'

plotting(s_name=Name, s_id=ID, s_type=SType, f_material=Material, f_type=FType)
