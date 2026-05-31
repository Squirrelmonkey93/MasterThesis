"""Search functions for different properties"""
# Importing global datasets
from combining_data import Finds, Sitesg

"""Site search: Name (Place-Toponym)"""
def site_name (S_name: str):
    sites_name = Sitesg.loc[Sitesg['Name'] == S_name]
    return sites_name

"""Site search: Site_ID"""
def site_id (S_id: str):
    sites_id = Sitesg.loc[Sitesg['SiteID'] == S_id]
    return sites_id

"""Site search: Site_type"""
def site_type (s_type: str, df=None):
    if df is None:
        df = Sitesg
    sites_type = df.loc[df['Site_type'] == s_type]
    return sites_type

"""Finds search: Material"""
def find_material (f_material: str, df=None):
    if df is None:
        df = Finds
    # Locating material type in the Finds dataframe
    material = df.loc[df['Material'] == f_material]
    # Locating the sites of these finds in the Sites dataframe
    finds_material = Sitesg.loc[Sitesg['Site_CID'].isin(material['Site_CID'])]
    return finds_material

"""Finds search: Type"""
def find_type (f_type: str, df=None):
    if df is None:
        df = Finds
    # Amphibian as it only had 6 entries, and thus was easily trackable
    # Locating material type in the Finds dataframe
    fi_type = df.loc[df['Type'] == f_type]
    # Locating the sites of these finds in the Sites dataframe
    finds_type = Sitesg.loc[Sitesg['Site_CID'].isin(fi_type['Site_CID'])]
    return finds_type

print(site_name('Bunnik-Fort Vechten'))
# print(site_id('7680'))
# print(site_type('rural settlement'))
# print(find_material('textiel'))
# print(find_type('amfibie'))