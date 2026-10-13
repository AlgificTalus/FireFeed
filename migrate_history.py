from pathlib import Path
import sqlite3

import geopandas as gpd

BASE_DIR = Path(__file__).parent
OLD_PATH = BASE_DIR / "or_wa_fires.gpkg"
NEW_PATH = BASE_DIR / "fire_history.db"

# Read the old history, including geometry
old = gpd.read_file(OLD_PATH, layer="fires")
print(f"Old history: {len(old)} rows")

# Keep only the attribute columns
history = old.drop(columns="geometry")

# Write them to a plain SQLite database
conn = sqlite3.connect(NEW_PATH)
history.to_sql("fires", conn, if_exists="replace", index=False)
conn.close()
print(f"Saved {len(history)} rows to {NEW_PATH.name}")