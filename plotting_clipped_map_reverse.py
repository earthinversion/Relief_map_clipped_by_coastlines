from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import netCDF4
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Path, PathPatch
from matplotlib.colors import LightSource



etopo_file = "/Users/utpalkumar50/Documents/bin/ETOPO1_Bed_g_gmt4.grd"

lonmin, lonmax = 119.5,122.5
latmin, latmax = 21.5,25.5


fig, ax = plt.subplots(figsize=(10,10))
map = Basemap(projection='merc',resolution = 'f', area_thresh = 10000., llcrnrlon=lonmin, llcrnrlat=latmin,urcrnrlon=lonmax, urcrnrlat=latmax)
f = netCDF4.Dataset(etopo_file)
try:
    lons = f.variables['lon'][:]
    lats = f.variables['lat'][:]
    etopo = f.variables['z'][:]
except:
    lons = f.variables['x'][:]
    lats = f.variables['y'][:]
    etopo = f.variables['z'][:]


lonmin,lonmax = lonmin-1,lonmax+1
latmin,latmax = latmin-1,latmax+1

lons_col_index = np.where((lons>lonmin) & (lons<lonmax))[0]
lats_col_index = np.where((lats>latmin) & (lats<latmax))[0]

etopo_sl = etopo[lats_col_index[0]:lats_col_index[-1]+1,lons_col_index[0]:lons_col_index[-1]+1]
lons_sl = lons[lons_col_index[0]:lons_col_index[-1]+1]
lats_sl = lats[lats_col_index[0]:lats_col_index[-1]+1]
lons_sl, lats_sl = np.meshgrid(lons_sl,lats_sl)

ls = LightSource(azdeg=315, altdeg=45)
rgb = ls.shade(np.array(etopo_sl), cmap=plt.cm.terrain, vert_exag=1, blend_mode=ls.blend_soft_light)

map.imshow(rgb,zorder=2,alpha=0.8,cmap=plt.cm.terrain, interpolation='bilinear')


map.drawcoastlines(color='k',linewidth=1,zorder=3)
map.drawcountries(color='k',linewidth=1,zorder=3)

parallelmin,parallelmax = int(latmin), int(latmax)+1
map.drawparallels(np.arange(parallelmin, parallelmax+1,0.5).tolist(),labels=[1,0,0,0],linewidth=0,fontsize=6)
meridianmin,meridianmax = int(lonmin),int(lonmax)+1
map.drawmeridians(np.arange(meridianmin, meridianmax+1,0.5).tolist(),labels=[0,0,0,1],linewidth=0,fontsize=6)
map.drawmapboundary(color='k', linewidth=2, zorder=1)



##getting all polygons used to draw the coastlines of the map
polys = [p.boundary for p in map.landpolygons]
##combining with map edges
polys = polys[:]
##creating a PathPatch
codes = [[Path.MOVETO]+[Path.LINETO for p in p[1:]] for p in polys]
verts = [v for p in polys for v in p]
codes = [xx for cs in codes for xx in cs]

path = Path(verts, codes)
patch = PathPatch(path,facecolor='white', edgecolor='none',zorder=4)

##masking the data outside the inland of taiwan
ax.add_patch(patch)


plt.savefig('station_map_masked_reverse.png',bbox_inches='tight',dpi=300)
plt.close('all')