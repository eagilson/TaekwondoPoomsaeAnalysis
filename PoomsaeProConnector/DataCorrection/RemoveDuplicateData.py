"""
Script to remove duplicate data from the SQLlite database after importing from the PoomasePro Access Databases.

Duplications from reusing the database on multiple days or events covered by this script.
"""

import sqlite3
import json
import pandas as pd
from itertools import combinations

# Connect to SQLite database
db_path = 'PoomsaeProConnector/PoomsaePro.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to remove duplicates from a table
def remove_duplicates(table_name, key_columns, event_name_filter, source_day, target_day):
    """
    Remove duplicate rows from target_day that match source_day data in the specified table.
    
    Args:
        table_name (str): Name of the table ('PoomsaeScores' or 'IndPoomsaeScores')
        key_columns (list): Columns to identify duplicates
        event_name_filter (str): Name of Event to update
        source_day (int): Source day (e.g., 1 for Day 1)
        target_day (int): Target day to remove duplicates from (e.g., 2 for Day 2)
    """
    key_columns_str = ', '.join([f't1.{col}' for col in key_columns])
    
    # Step 1: Identify duplicates by joining source_day and target_day data
    query_create_temp = f"""
    CREATE TEMPORARY TABLE temp_duplicates AS
    SELECT t1.DatabaseID AS target_db, t1.Performance_ID AS target_perf_id
    FROM {table_name} t1
    JOIN Events e1 ON t1.DatabaseID = e1.DatabaseID
    JOIN {table_name} t2 ON t1.CompetitorNbr = t2.CompetitorNbr
        AND t1.RoundName = t2.RoundName
        AND t1.Division = t2.Division
        AND t1.Gender = t2.Gender
        AND t1.Category = t2.Category
    JOIN Events e2 ON t2.DatabaseID = e2.DatabaseID
    WHERE e1.EventName LIKE '%{event_name_filter}%'
        AND e1.CompDay = {target_day}
        AND e2.EventName LIKE '%{event_name_filter}%'
        AND e2.CompDay = {source_day}
        AND t1.DatabaseID != t2.DatabaseID;
    """
    cursor.execute(query_create_temp)
    
    # Step 2: Delete duplicate rows from target_day
    query_delete = f"""
    DELETE FROM {table_name}
    WHERE (DatabaseID, Performance_ID) IN (
        SELECT target_db, target_perf_id FROM temp_duplicates
    );
    """
    cursor.execute(query_delete)
    
    # Step 3: Drop temporary table
    cursor.execute("DROP TABLE IF EXISTS temp_duplicates")
    
    # Commit changes
    conn.commit()
    
    # Step 4: Verify no duplicates remain
    query_verify = f"""
    SELECT t1.DatabaseID, t1.Performance_ID, {key_columns_str}, COUNT(*) as count
    FROM {table_name} t1
    JOIN Events e1 ON t1.DatabaseID = e1.DatabaseID
    JOIN {table_name} t2 ON t1.CompetitorNbr = t2.CompetitorNbr
        AND t1.RoundName = t2.RoundName
        AND t1.Division = t2.Division
        AND t1.Gender = t2.Gender
        AND t1.Category = t2.Category
    JOIN Events e2 ON t2.DatabaseID = e2.DatabaseID
    WHERE e1.EventName LIKE '%{event_name_filter}%'
        AND e1.CompDay = {target_day}
        AND e2.EventName LIKE '%{event_name_filter}%'
        AND e2.CompDay = {source_day}
        AND t1.DatabaseID != t2.DatabaseID
    GROUP BY t1.DatabaseID, t1.Performance_ID, {key_columns_str}
    HAVING count > 1;
    """
    df = pd.read_sql_query(query_verify, conn)
    if df.empty:
        print(f"No duplicates remain in {table_name} for Day {source_day} in Day {target_day} for {event_name_filter}.")
    else:
        print(f"Warning: Duplicates still exist in {table_name} for Day {source_day} in Day {target_day}:\n", df)


def event_days(event_name: str) -> list:
    """
    Returns list of days for the given event.
    
    Args:
        event_name (str): Name of event
    
    Returns:
        (list): list of days
    """

    query_event_days = f"""
        SELECT DISTINCT CompDay 
        FROM Events
        WHERE EventName = '{event_name}'
    """

    cursor.execute(query_event_days)
    days = [row[0] for row in cursor.fetchall()]
    return days

#read DuplicateEvents.JSON for list of events with duplicate data
with open('data/DuplicateEvents.JSON','r') as file:
    events = json.load(file)
    file.close()

for event in events:
    #days in event
    days = event_days(event['event'])

    #all possible unordered pairs of days
    day_pairs = list(combinations(days, 2))
    for table in event['table']:
        for pair in day_pairs:
            remove_duplicates(table['table_name'], table['key_columns'], event['event'], pair[0], pair[1])

# Close connection
conn.close()