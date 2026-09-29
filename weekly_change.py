from pathlib import Path
import sqlite3

import pandas as pd

# Show every column and use the full terminal width when printing tables
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# --- Settings ---
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "or_wa_fires.gpkg"

# --- Shared snapshots ---
# Both queries below need the same three named tables:
#   week:       every row from the last 7 days
#   first_run:  the fires from the earliest run this week
#   latest_run: the fires from the most recent run
SNAPSHOTS = """
WITH week AS (
    SELECT name, state, acres, pct_contained, run_time
    FROM fires
    WHERE run_time >= datetime('now', '-7 days')
),
first_run AS (
    SELECT * FROM week
    WHERE run_time = (SELECT MIN(run_time) FROM week)
),
latest_run AS (
    SELECT * FROM week
    WHERE run_time = (SELECT MAX(run_time) FROM week)
)
"""

# --- Query 1: how each current fire changed this week ---
# Start from the latest run and match each fire to its first-run record.
# Fires that started mid-week have blank starting values.
changes_query = SNAPSHOTS + """
SELECT
    l.name,
    l.state,
    f.acres AS start_acres,
    l.acres AS end_acres,
    ROUND((l.acres - f.acres) * 100.0 / NULLIF(f.acres, 0), 1) AS pct_change,
    f.pct_contained AS start_contained,
    l.pct_contained AS end_contained,
    l.pct_contained - f.pct_contained AS contained_change
FROM latest_run AS l
LEFT JOIN first_run AS f
    ON l.name = f.name AND l.state = f.state
ORDER BY CONTAINED_CHANGE DESC
"""

# --- Query 2: fires that dropped out this week ---
# Start from the first run and keep the fires with no match in the latest run.
dropped_query = SNAPSHOTS + """
SELECT f.name, f.state, f.acres, f.pct_contained
FROM first_run AS f
LEFT JOIN latest_run AS l
    ON f.name = l.name AND f.state = l.state
WHERE l.name IS NULL
"""

# --- Run both queries ---
conn = sqlite3.connect(DB_PATH)

changes = pd.read_sql_query(changes_query, conn)
dropped = pd.read_sql_query(dropped_query, conn)

conn.close()

print("Changes this week:")
print(changes)
print()
print(f"Fires that dropped out this week: {len(dropped)}")
print(dropped)