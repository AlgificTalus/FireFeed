import sqlite3
import pandas as pd
DATA_PATH = r'C:\Conda_Projects\FireFeed\or_wa_fires.gpkg'
conn = sqlite3.connect(DATA_PATH)
query= "SELECT run_time, COUNT(*) as n_fires FROM fires GROUP BY run_time"
df = pd.read_sql(query,conn)
print(df)
conn.close()