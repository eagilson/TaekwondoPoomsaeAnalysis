import pandas as pd
from utils.PoomsaeProCleaning import load_data, categorize_division, translate_simultaneous, draw_type

def build_database(db_path: str, sql_file_path: str) -> pd.DataFrame:

    # Load data
    df = load_data(db_path, sql_file_path)

    # Data cleaning
    df = df.dropna(subset=['Winner', 'Simultaneous', 'Division', 'EventName'])

    # Translate Simultaneous flag
    df['Simultaneous'] = df['Simultaneous'].apply(translate_simultaneous)

    # Categorize divisions
    df['division_category'] = df['Division'].apply(categorize_division)
    df['division_group'] = df['division_category'].apply(lambda x: 'Pair & Team' if x in ['Pair', 'Team'] else 'Individual')

    # Random draw or Designated Poomsae
    df['draw_type'] = df['Poomsae1'].apply(draw_type)

    return df