from config import Site_csv, SiteType_csv, Finds_csv, NL_boundary
import pandas as pd
import geopandas as gpd

# Loading in starting data sets with specific columns
Site = pd.read_csv(Site_csv, usecols=['SiteID', 'Place', 'Toponym'])
SiteType = pd.read_csv(SiteType_csv, usecols=['SiteID', 'Site_subID', 'X-coordinate_RD', 'Y-coordinate_RD', 'Site_type'])
Find1 = pd.read_csv(Finds_csv, usecols=['FindID', 'SiteID', 'Site_subID', 'Material', 'Type'])
NL = gpd.read_file(NL_boundary)

# Combining two columns to create 1 Name column
Site['Name'] = Site['Place'] + '-' + Site['Toponym']

# Combining both data sets with site information into one
# Remove unnecessary columns of place
Sites = pd.merge(Site, SiteType, on='SiteID')
Sites = Sites.drop(columns=['Place', 'Toponym'])

"""Getting df from sites to give them an 'entire site' (-1) value.
Mostly used for Finds not assigned to specific subsite"""
def site_null (df):
    # Copying entire Sites dataframe
    df_null = df.copy()
    # Getting unique SiteID's
    snull = df_null['SiteID'].unique()
    # Removing duplicate items, so each site only has one entry
    df_null = df_null[df_null['SiteID'].isin(snull)].drop_duplicates(subset=['SiteID'])
    # Replacing Site_subID with the 'unassigned to subsite' number of -1
    df_null.loc[df_null['Site_subID'] > 0, 'Site_subID'] = -1
    return df_null
Site_null = site_null(Sites)

"""Creating combined ID for the sites"""
def sites_cid (df):
    # Combining SiteID (1) and Site_subID (1) to a Site combined ID (SiteCID) (1.1)
    df['SiteID'] = df['SiteID'].astype(str)
    df['Site_subID'] = df['Site_subID'].astype(str)
    df['Site_CID'] = df['SiteID'] + '.' + df['Site_subID']
    # Remove separate subID column
    df = df.drop(columns=['Site_subID'])

    # Renaming columns for easier access
    df = df.rename(columns={'X-coordinate_RD': 'X', 'Y-coordinate_RD': 'Y'})
    # Reordering columns to: SiteID, Site_CID, Name, Site_type, X, Y
    df = df.iloc[:, [0, 5, 1, 4, 2, 3]]
    return df
Sites = sites_cid(Sites)
Site_null = sites_cid(Site_null)

"""Creating combined ID for the finds"""
def finds_cid (df):
    # Filling NaN and 0 values with the unassigned number
    df['Site_subID'] = df['Site_subID'].fillna(-1)
    df.loc[df['Site_subID'] == 0, 'Site_subID'] = -1

    # Combining SiteID and Site_subID to Site combined ID (SiteCID)
    # First subID to integer (from float) to remove decimals
    df['Site_subID'] = df['Site_subID'].astype(int)
    df['SiteID'] = df['SiteID'].astype(str)
    df['Site_subID'] = df['Site_subID'].astype(str)
    df['Site_CID'] = df['SiteID'] + '.' + df['Site_subID']
    # Remove separate subID column
    df = df.drop(columns=['Site_subID'])
    # Reordering columns to: SiteID, Site_CID, FindID, Material, Type
    df = df.iloc[:, [1, 4, 0, 2, 3]]
    return df
Find1 = finds_cid(Find1)

# Option to save the null sites to a csv-file
# Site_null.to_csv('created_csv/Sites_null.csv')

# Combining the original Sites with the unassigned subsites
Sites = pd.concat([Sites, Site_null], ignore_index=True)

# Transforming dataframe into a geo-dataframe
Sites = gpd.GeoDataFrame(Sites, geometry=gpd.points_from_xy(Sites.X, Sites.Y), crs="EPSG:28992")
# print(Sitesg.head())

NL_geom = NL.geometry
NL_union = NL_geom.union_all()
Sites = Sites.loc[Sites['geometry'].within(NL_union)]
# Sites.to_file('created_gpkgs/Sites.gpkg', driver ='GPKG', layer='name')

# Only using Finds that have a SiteID that is also found in Site
Find2 = Find1[Find1['Site_CID'].isin(Sites['Site_CID'])]
# Option to save the cleaned up Finds to a csv-file
# Finds.to_csv('created_csv/cleanFinds.csv')

Finds = Sites.merge(Find2, on=['SiteID', 'Site_CID'], how='left')

Finds = gpd.GeoDataFrame(Finds)
Finds['FindID'] = Finds['FindID'].astype('Int64')
print('Data combined')