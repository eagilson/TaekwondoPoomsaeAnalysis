# Categorize event
def categorize_event(event):
    match event.lower():
        case str(s) if 'freestyle' in s:
            return 'Freestyle'
        case str(s) if 'demo' in s:
            return 'Demo'
        case str(s) if 'para' in s:
            return 'Para'
        case str(s) if 'mixed' in s:
            return 'Mixed'
        case _:
            return 'Recognized'

# Load data from SQLite
def load_data(db_path, sql):
    import sqlite3
    from pathlib import Path
    import pandas as pd

    try:
        if not Path(db_path).exists():
            print(f"Error: Database '{db_path}' not found.")
            return None
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
def categorize_division(division):
    """
    Categorize a division name into 'Pair & Team' or 'Individual'.
    
    Args:
        division (str): The division name (e.g., 'Pair Senior', 'Team Junior', 'Individual Open').
        
    Returns:
        str: 'Pair & Team' if division contains 'Pair' or 'Team' (case-insensitive), else 'Individual'.
    """
    if not isinstance(division, str):
        return 'Individual'
    match division.lower():
        case str(s) if 'pair' in s:
            return 'Pair'
        case str(s) if 'team' in s:
            return 'Team'
        case _:
            return 'Individual'