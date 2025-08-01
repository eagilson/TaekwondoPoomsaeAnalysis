# Load data from SQLite
def load_data(db_path, sql_file_path):
    import sqlite3
    from pathlib import Path
    import pandas as pd

    if not Path(db_path).exists():
        print(f"Error: Database '{db_path}' not found.")
        return None
    if not Path(sql_file_path).exists():
        print(f"Error: SQL file '{sql_file_path}' not found.")
        return None
    try:
        with open(sql_file_path, 'r') as file:
            sql_query = file.read()
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


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
        
def categorize_belt(category):
    match category.lower():
        case str(s) if 'yellow' in s:
            return 'Yellow'
        case str(s) if 'green' in s:
            return 'Green'
        case str(s) if 'blue' in s:
            return 'Blue'
        case str(s) if 'red' in s:
            return 'Red'
        case _:
            return 'Black'
        
def extract_age(text):
    # Find positions of hyphen and [
    hyphen_pos = text.find('-')
    bracket_pos = text.find('[')
    
    # If no [ is found, set end to the length of the string
    end = bracket_pos if bracket_pos != -1 else len(text)
    
    # If hyphen is before [ (or [ is not found), start after hyphen; otherwise, start at 0
    start = hyphen_pos + 1 if hyphen_pos != -1 and (bracket_pos == -1 or hyphen_pos < bracket_pos) else 0
    
    # Extract substring and trim spaces
    return text[start:end].strip()