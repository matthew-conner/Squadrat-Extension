
# Full script with corrected bounds/center/index block
# Requires: geopandas, shapely, networkx, numpy, matplotlib, fiona, pyproj, pandas
import geopandas as gpd
import networkx as nx
import numpy as np
from shapely.geometry import box
import matplotlib.pyplot as plt
import os
import pandas as pd

INPUT_KML = "squadrats-2025-11-03.kml"   # replace or point to uploaded file
OUT_DIR = "yardinho_output"
os.makedirs(OUT_DIR, exist_ok=True)

# 1) load file (try KML driver; GeoPandas can usually read KML/KMZ)
try:
    gdf = gpd.read_file(INPUT_KML, driver="KML")
except Exception as e:
    # fallback automatic read
    gdf = gpd.read_file(INPUT_KML)

if gdf.empty:
    raise SystemExit("Input file contains no features. Check the layer or file.")

# If the features are points, buffer to polygon by cell size estimate (rare)
if gdf.geometry.iloc[0].geom_type == "Point":
    # estimate spacing from distances between points
    pts = gdf.geometry.centroid
    if len(pts) > 1:
        dists = []
        coords = np.array([p.coords[0] for p in pts])
        for i in range(1, min(len(coords), 200)):
            dists.append(np.hypot(*(coords[i] - coords[0])))
        approx = np.median(dists) if dists else 10
    else:
        approx = 10
    gdf['geometry'] = gdf.geometry.buffer(approx/2)

#Plotting
gdf_squads = gdf[(gdf['Name'] == 'squadratinhos')]
gdf_ll = gdf_squads.to_crs(epsg=4326)

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt

fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection=ccrs.PlateCarree())
gdf_ll.plot(ax=ax, color='tab:orange', edgecolor='k', transform=ccrs.PlateCarree())

# Set bounds (Swiss lon/lat)
ax.set_xlim([6, 6.4])
ax.set_ylim([46.25, 46.55])

ax.set_title("Multipolygon: 'squadratinhos'")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
