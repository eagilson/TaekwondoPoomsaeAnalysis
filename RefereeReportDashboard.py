import pandas as pd
import sqlite3
import panel as pn
from pathlib import Path

# Load data from SQLite
def load_data(db_path, sql):
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
    
def create_dashboard(db_path, sql, event='All',referee='All'):
    df = load_data(db_path, sql)
    if df is None:
        return pn.pane.Markdown("Error: Failed to load data.")
    
    # Calculate difference
    diff_col = 'AccDifference'
    df[diff_col] = df['TotalAccuracy'] - df['Accuracy']

    diff_col = 'PresDifference'
    df[diff_col] = df['TotalPresentation'] - df['Presentation']

    diff_col = ['AccDifference','PresDifference']

    # Generate summary statistics grouped by name
    group_by = ['EventName','Division','Gender','Category','Round','RefereeName']
    stats = df.groupby(group_by)[diff_col].agg(['mean', 'std', 'min', 'max', 'count']).reset_index()
    #print(stats)
    #stats.columns = [group_by] + [f"{stat}" for stat in stats.columns[1:]]

    # Filter DataFrame
    filtered_df = stats if event == 'All' else stats[stats['EventName'] == event]
    filtered_df = filtered_df if referee == 'All' else filtered_df[filtered_df['RefereeName'] == referee]

    # Create a styled DataFrame with hidden index
    df_styled = filtered_df.style.hide(axis='index')

    # Create table
    table = pn.widgets.DataFrame(filtered_df,show_index=False , name='Summary Statistics', width=1200)

    return pn.Column(table)

#Builds the Event Table
with open('sql/RefereeAccPres.sql','r') as file:
    sql = file.read()
    file.close()

poomsaeprodb = 'PoomsaeProConnector/PoomsaePro.db'

# Create Event dropdown
Event_select = pn.widgets.Select(
    name='Filter by Event',
    options=['All'] + list(load_data(poomsaeprodb,sql)['EventName'].unique()),
    value='All'
)

# Create Referee dropdown
Referee_select = pn.widgets.Select(
    name="Filter by Referee",
    options=["All"] + list(load_data(poomsaeprodb,sql)["RefereeName"].unique()),
    value="All"
)

# Bind dropdown to dashboard
dashboard = pn.bind(create_dashboard, event=Event_select, referee=Referee_select,
                     db_path=poomsaeprodb, sql=sql)

# Layout
layout = pn.Column(
    pn.pane.Markdown("Poomsae Referee Analysis"),
    Event_select,
    Referee_select,
    dashboard
)

# Serve the dashboard
layout.servable()

#panel serve RefereeReportDashboard.py --show

