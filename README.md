# FireFeed

A Python pipeline that pulls current wildfire perimeters for Oregon and Washington every day, keeps a daily history of each fire's size and containment, and maps the results.

**Live map:** [algifictalus.github.io/FireFeed/fire_map.html](https://algifictalus.github.io/FireFeed/fire_map.html)

## What it does

`fetch.py` requests current fire perimeters from the National Interagency Fire Center's WFIGS Current Interagency Fire Perimeters dataset through its ArcGIS REST API. It filters the data to fires that started in Oregon and Washington, keeps the fire name, state, acreage, and percent containment, and stamps each run with a UTC timestamp. Each run produces three outputs:

- `fire_history.db`: a SQLite database where each run's fire attributes are appended, building a daily history for SQL queries. Geometry is left out to keep the file small.
- `or_wa_fires.gpkg`: a GeoPackage of the current fire perimeters, simplified and replaced each run.
- `fire_map.html`: an interactive web map with fires colored by percent containment and tooltips showing each fire's name, size, and containment.

The script runs automatically every day through GitHub Actions, which commits the updated outputs back to this repository and republishes the map through GitHub Pages.

`query.py` uses SQL to query the fire history, for example counting fires per run.

`weekly_change.py` joins the week's first and latest snapshots to report acreage change, containment change, and fires that dropped out of the dataset.

## Design note

The first version appended full-detail perimeters to a GeoPackage on every run. The file grew by several megabytes a day and passed GitHub's 100 MB file limit after about two weeks. The history now stores attributes only, and the perimeter GeoPackage is simplified and overwritten each run, bringing it from about 103 MB to under 500 KB.

## Tools

- Python
- requests (API calls)
- geopandas (spatial data handling)
- folium and branca (web mapping and color scale)
- SQLite and SQL (fire history and queries)
- GitHub Actions (daily scheduling) and GitHub Pages (map hosting)
- USGS National Map basemap tiles

## How to run it

1. Install the required packages:
   `pip install -r requirements.txt`
2. Run `fetch.py` to collect the latest fire data and update the outputs.
3. Run `query.py` or `weekly_change.py` to query the stored history.