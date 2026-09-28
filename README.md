# FireFeed

A Python script that pulls current wildfire perimeters for Oregon and Washington, stores each run in a spatial database, and maps the results.

## What it does

`fetch.py` requests current fire perimeters from the National Interagency Fire Center's WFIGS Current Interagency Fire Perimeters dataset through its ArcGIS REST API. It filters the data to fires that started in Oregon and Washington, keeps the fire name, state, acreage, and percent containment, and adds a timestamp for the run.

Each run is appended to a GeoPackage database, so the data builds a history over time. The script also produces an interactive web map (`fire_map.html`) of the current fires, with tooltips showing each fire's name, size, and containment.

`query.py` uses SQL to query the fire history in the GeoPackage, for example counting fires per run or filtering by state and size.

## Tools

- Python
- requests (API calls)
- geopandas (spatial data handling)
- folium (web mapping)
- SQLite and SQL (querying the GeoPackage)
- USGS National Map basemap tiles

## How to run it

1. Install the required packages:
   `pip install geopandas requests folium`
2. Update the file paths in the Settings section of each script to match your system.
3. Run `fetch.py` to collect the latest fire data and update the map.
4. Run `query.py` to query the stored history.

## Next steps

- Run the script automatically on a daily schedule
- Host the map online so it updates on its own
- Add queries that track fire growth and containment over time