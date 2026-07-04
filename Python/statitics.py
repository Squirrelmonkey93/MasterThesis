import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

"""Chi Squared test on palaeogeography and site counts"""
# currently only Dutch river area, as only access to that palaeogeography file in QGIS.
palaeogeo = gpd.read_file("gpkgs/count_palaeogeo.gpkg")
pgeo = pd.DataFrame(palaeogeo.drop(columns=['simplified', 'walk coeff','geometry']))
pgeo = pgeo.rename(columns={'NUMPOINTS': 'count_obs'})
pgeo['area%'] = (pgeo['Area']/pgeo['Area'].sum())
pgeo['count_exp'] = pgeo['count_obs'].sum()*pgeo['area%']
pgeo['site_density'] = pgeo['count_obs']/pgeo['Area']
pgeo.reset_index()

# print(pgeo.site_density)
pgeo.plot.bar(x='element', y='site_density')
plt.xlabel("palaeogeography element")
plt.ylabel("site density")

plt.show()
# from scipy.stats import chisquare
# print(chisquare(pgeo.count_obs, pgeo.count_exp, ddof=17))

print(pgeo['count_obs'].sum())
