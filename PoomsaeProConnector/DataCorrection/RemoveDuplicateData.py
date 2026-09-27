"""
Script to remove duplicate data from the SQLite database after importing
from the PoomsaePro Access Databases.

Duplications from reusing the database on multiple days or events
are covered by this script.

Join conditions between t1 and t2 are built from key_columns so the
ON clause stays in sync with the configured match fields.

Keeper rule: keep the earliest CompDay row that has a valid score
(score columns <> -1). That is the day the scores were entered.
Later-day copies of the same performance are deleted even if they
also contain the scores. Rows with only placeholder scores (-1) are
not kept when a valid-score copy exists.
"""

import json
import sqlite3

import pandas as pd

# Connect to SQLite database
db_path = "PoomsaeProConnector/PoomsaePro.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Columns used to decide whether a performance has real scores.
# -1 is the PoomsaePro placeholder for "not scored".
SCORE_COLUMNS = (
    "Full_Score",
    "Form_Score_AB",
    "Form_Score_A",
    "Acc_Avg_A",
    "Pre_Avg_A",
)


def join_on_key_columns(key_columns):
    """
    Build the ON clause comparing t1 and t2 on every key column.

    Args:
        key_columns (list): Column names used to identify duplicates.

    Returns:
        str: SQL fragment such as
             "t1.CompetitorNbr = t2.CompetitorNbr AND t1.RoundName = t2.RoundName"
    """
    if not key_columns:
        raise ValueError("key_columns must contain at least one column")
    return " AND ".join(f"t1.{col} = t2.{col}" for col in key_columns)


def table_score_columns(table_name):
    """Return SCORE_COLUMNS that actually exist on table_name."""
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing = {row[1] for row in cursor.fetchall()}
    cols = [col for col in SCORE_COLUMNS if col in existing]
    if not cols:
        raise ValueError(f"No score columns found on {table_name}")
    return cols


def score_predicate(alias, score_columns):
    """True when any score column on alias is not NULL and not -1."""
    parts = [f"({alias}.{col} IS NOT NULL AND {alias}.{col} <> -1)" for col in score_columns]
    return "(" + " OR ".join(parts) + ")"


def remove_duplicates(table_name, key_columns, event_name_filter):
    """
    Within one event, find performances that appear under more than one
    DatabaseID (day/ring). Keep the earliest CompDay row that has valid
    scores. Delete every other copy.

    If no copy has valid scores, keep the earliest CompDay row so
    placeholder-only groups are not wiped out.
    """
    join_on = join_on_key_columns(key_columns)
    key_columns_str = ", ".join(f"t1.{col}" for col in key_columns)
    score_cols = table_score_columns(table_name)
    t1_valid = score_predicate("t1", score_cols)
    t2_valid = score_predicate("t2", score_cols)

    cursor.execute("DROP TABLE IF EXISTS temp_duplicates")

    # For each target row t1, decide whether a better keeper exists as t2:
    #   1. t2 has valid scores and t1 does not, or
    #   2. both valid (or both invalid) and t2.CompDay < t1.CompDay, or
    #   3. same validity and same CompDay and t2.DatabaseID < t1.DatabaseID
    # Those t1 rows are the copies to delete.
    query_create_temp = f"""
    CREATE TEMPORARY TABLE temp_duplicates AS
    SELECT DISTINCT t1.DatabaseID AS target_db, t1.Performance_ID AS target_perf_id
    FROM {table_name} t1
    JOIN Events e1 ON t1.DatabaseID = e1.DatabaseID
    JOIN {table_name} t2 ON {join_on}
    JOIN Events e2 ON t2.DatabaseID = e2.DatabaseID
    WHERE e1.EventName LIKE '%' || ? || '%'
      AND e2.EventName LIKE '%' || ? || '%'
      AND t1.DatabaseID != t2.DatabaseID
      AND (
            ({t2_valid} AND NOT {t1_valid})
         OR ({t2_valid} = {t1_valid} AND e2.CompDay < e1.CompDay)
         OR ({t2_valid} = {t1_valid} AND e2.CompDay = e1.CompDay
             AND t2.DatabaseID < t1.DatabaseID)
      );
    """
    cursor.execute(query_create_temp, (event_name_filter, event_name_filter))

    cursor.execute("SELECT COUNT(*) FROM temp_duplicates")
    n_delete = cursor.fetchone()[0]

    query_delete = f"""
    DELETE FROM {table_name}
    WHERE (DatabaseID, Performance_ID) IN (
        SELECT target_db, target_perf_id FROM temp_duplicates
    );
    """
    cursor.execute(query_delete)
    conn.commit()

    cursor.execute("DROP TABLE IF EXISTS temp_duplicates")

    query_verify = f"""
    SELECT {key_columns_str}, COUNT(DISTINCT t1.DatabaseID) AS db_count
    FROM {table_name} t1
    JOIN Events e1 ON t1.DatabaseID = e1.DatabaseID
    JOIN {table_name} t2 ON {join_on}
    JOIN Events e2 ON t2.DatabaseID = e2.DatabaseID
    WHERE e1.EventName LIKE '%' || ? || '%'
      AND e2.EventName LIKE '%' || ? || '%'
      AND t1.DatabaseID != t2.DatabaseID
    GROUP BY {key_columns_str}
    HAVING db_count > 1;
    """
    df = pd.read_sql_query(
        query_verify, conn, params=(event_name_filter, event_name_filter)
    )
    print(
        f"{table_name} / {event_name_filter}: deleted {n_delete} duplicate row(s)."
    )
    if df.empty:
        print(
            f"No cross-day/ring duplicates remain in {table_name} "
            f"for {event_name_filter}."
        )
    else:
        print(
            f"Warning: duplicate key groups still exist in {table_name} "
            f"for {event_name_filter}:\n",
            df,
        )


# Read DuplicateEvents.JSON for list of events with duplicate data
with open("data/DuplicateEvents.JSON", "r") as file:
    events = json.load(file)

for event in events:
    for table in event["table"]:
        remove_duplicates(
            table["table_name"],
            table["key_columns"],
            event["event"],
        )

conn.close()
