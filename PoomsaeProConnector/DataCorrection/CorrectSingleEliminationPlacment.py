"""
This script corrects the Placement of athletes in Single Elimination divisions that are Pre-2024.

Pre-2025 Poomsae Pro databases do not have a completed placement column for Single Elimination rounds.
The Post-2025 convention is the loser's place is populated. The winner's place is 0 when not in Round of 2 or 1 when in Round of 2.
"""

import sqlite3
import pandas as pd

# Connect to SQLite database
db_path = 'PoomsaeProConnector/PoomsaePro.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def execute_sql(sql_file_path: str):
    """
    Executes SQL statement.
    
    Args:
        sql_file_path (str): relative string of the file path for the SQL query file.
    """

    with open(sql_file_path, 'r') as file:
        sql_query = file.read()
        cursor.execute(sql_query)
        conn = sqlite3.connect(db_path)
        conn.close()

# Round of 4 and up
# If the athlete has a match in the next round they stay as 0
# If the athlete does not have a match in the next round Placement to N in Round of N
sql_file_path = 'PoomsaeProConnector/DataCorrection/sql/UpdateSingleEliminationPlacement.sql'
execute_sql(sql_file_path)

# Round of 2 codes
# Update Winner to 1 in Round of 2
# Update the Loser to 2 in Round of 2
sql_file_path = 'PoomsaeProConnector/DataCorrection/sql/UpdateSingleEliminationPlacementR2.sql'
execute_sql(sql_file_path)

# 2021 data might have other issues related to round numbering