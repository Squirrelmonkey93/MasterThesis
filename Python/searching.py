"""Search functions for different properties"""
# Importing global datasets
from combining_data import Finds, Sites

"""Site search: Name (Place-Toponym)"""
def site_name (S_name: str):
    sites_name = Sites.loc[Sites['Name'] == str(S_name)]
    return sites_name

"""Site search: Site_ID"""
def site_id (S_id: str):
    sites_id = Sites.loc[Sites['SiteID'] == str(S_id)]
    return sites_id

"""Site search: Site_type"""
def site_type (s_type: str, df=None):
    if df is None:
        df = Sites
    sites_type = df.loc[df['Site_type'] == str(s_type)]
    return sites_type

"""Finds search: Material"""
def find_material (f_material: str, df=None):
    if df is None:
        df = Finds
    # Locating material type in the Finds dataframe
    material = df.loc[df['Material'] == str(f_material)]
    # Locating the sites of these finds in the Sites dataframe
    finds_material = Sites.loc[Sites['Site_CID'].isin(material['Site_CID'])]
    return finds_material

"""Finds search: Type"""
def find_type (f_type: str, df=None):
    if df is None:
        df = Finds
    # Amphibian as it only had 6 entries, and thus was easily trackable
    # Locating material type in the Finds dataframe
    fi_type = df.loc[df['Type'] == str(f_type)]
    # Locating the sites of these finds in the Sites dataframe
    finds_type = Sites.loc[Sites['Site_CID'].isin(fi_type['Site_CID'])]
    return finds_type

print(site_name('Bunnik-Fort Vechten').columns)
# print(site_id('502'))
# print(site_type('rural settlement'))
# print(find_material('textiel'))
# print(find_type('amfibie'))
print('Search complete')
