# FireFeed

A Python pipeline that pulls current wildfire perimeters for Oregon and Washington every day, stores each run in a spatial database, and maps the results.

## What it does

`fetch.py` requests current fire perimeters from the National Interagency Fire Center's WFIGS Current Interagency Fire Perimeters dataset through its ArcGIS REST API. It filters the data to fires that started in Oregon and Washington, keeps the fire name, state, acreage, and percent containment, and adds a UTC timestamp for the run.

Each run is appended to a GeoPackage database, so the data builds a history over time. The script also produces an interactive web map (`fire_map.html`) with fires colored by percent containment and tooltips showing each fire's name, size, and containment. Perimeters are simplified for the web map to keep the file small, while full-detail geometry is kept in the database.

The script runs automatically every day through GitHub Actions, which commits the updated database and map back to this repository.

`query.py` uses SQL to query the fire history in the GeoPackage, for example counting fires per run or filtering by state and size.

## Tools

- Python
- requests (API calls)
- geopandas (spatial data handling)
- folium and branca (web mapping and color scale)
- SQLite and SQL (querying the GeoPackage)
- GitHub Actions (daily scheduling)
- USGS National Map basemap tiles

## How to run it

1. Install the required packages:
   `pip install -r requirements.txt`
2. Run `fetch.py` to collect the latest fire data and update the map.
3. Run `query.py` to query the stored history.

## 
- weekly_change.py joins the week's first and latest snapshots to report acreage change, containment change, and fires that dropped out of the dataset.

- **Live map:** [algifictalus.github.io/FireFeed/fire_map.html](https://algifictalus.github.io/FireFeed/fire_map.html)