from datetime import datetime, timezone
from pathlib import Path

import folium
import geopandas as gpd
import requests
import branca.colormap as cm


# --- Settings ---
URL = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters_Current/FeatureServer/0/query"
# Query options sent to the NIFC server. requests turns this dictionary into
# the ?key=value&key=value part of the URL and handles the encoding.
#   where:     SQL-style filter; "1=1" is always true, so it returns every fire
#   outFields: which attribute columns to return; "*" means all of them
#   f:         output format
PARAMS = {"where": "1=1", "outFields": "*", "f": "geojson"}
STATES = ["US-OR", "US-WA"]
MAP_CENTER = [45.5, -120.5]
TILES = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}"
TILES_ATTR = "USGS The National Map"
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "or_wa_fires.gpkg"
MAP_PATH = BASE_DIR / "fire_map.html"
# Simplification tolerance for the web map, in degrees (0.001 is roughly 100 m)
MAP_SIMPLIFY = 0.001

# --- Fetch ---
response = requests.get(URL, params=PARAMS)
print(f"Status code: {response.status_code}")
data = response.json()
features = data["features"]

# --- Clean ---
gdf = gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")
cols = ["poly_IncidentName", "attr_POOState", "poly_GISAcres", "attr_PercentContained", "geometry"]
gdf = gdf[cols]
gdf = gdf[gdf["attr_POOState"].isin(STATES)]
gdf = gdf.rename(columns={
    "poly_IncidentName": "name",
    "attr_POOState": "state",
    "poly_GISAcres": "acres",
    "attr_PercentContained": "pct_contained"
})
gdf["acres"] = gdf["acres"].round(0)
print(f"{len(gdf)} fires in {STATES}")

# --- Save ---
run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
gdf["run_time"] = run_time
if DB_PATH.exists():
    gdf.to_file(DB_PATH, layer="fires", mode="a")
else:
    gdf.to_file(DB_PATH, layer="fires", mode="w")

# --- Map ---
# Simplify a copy of the perimeters so the HTML file stays small.
# The full-detail geometry is still what gets saved to the database above.

colormap = cm.LinearColormap(
    colors=["red", "orange", "green"],
    vmin=0,
    vmax=100,
    caption="% Contained"
)
def style_fire(feature):
    pct = feature["properties"]["pct_contained"]
    if pct is None:
        color = "gray"
    else:
        color = colormap(pct)
    return {"color": color, "fillColor": color, "weight": 1, "fillOpacity": 0.6}

map_gdf = gdf.copy()
map_gdf["geometry"] = map_gdf.geometry.simplify(MAP_SIMPLIFY)

m = folium.Map(location=MAP_CENTER, zoom_start=6, tiles=TILES, attr=TILES_ATTR)
folium.GeoJson(
    map_gdf,
    style_function=style_fire,
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "acres", "pct_contained"],
        aliases=["Fire:", "Acres:", "% Contained:"]
    )
).add_to(m)
colormap.add_to(m)
m.save(MAP_PATH)