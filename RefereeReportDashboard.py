import pandas as pd
import sqlite3
import panel as pn
from pathlib import Path


#Categorize event
#Recognized, Demo, Para, Freestyle
#Does not include Single Exlimination or Simultaneous 
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

def create_dashboard(db_path, sql, competition = 'All',event='All',referee='All'):
    df = load_data(db_path, sql)
    if df is None:
        return pn.pane.Markdown("Error: Failed to load data.")
    
    #Categorize Division
    df['Division_category'] = df['Division'].apply(categorize_event)
    
    # Calculate difference
    diff_col = 'AccDifference'
    df[diff_col] = df['Accuracy'] - df['TotalAccuracy']

    diff_col = 'PresDifference'
    df[diff_col] = df['Presentation'] - df['TotalPresentation']

    diff_col = ['AccDifference','PresDifference']

    #Event filter before grouping
    df = df if event == 'All' else df[df['Division_category'] == event]

    # Generate summary statistics grouped by name
    group_by = ['EventName','Division','Gender','Category','Round','RefereeName']
    stats = df.groupby(group_by).agg({'RingNbr':'count',
                                      'AccDifference':['mean', 'std'],
                                      'PresDifference':['mean', 'std']}).reset_index()
    
    # Flatten the MultiIndex and rename the RingNbr count column
    stats.columns = ['_'.join(col).strip() if col[1] else col[0] for col in stats.columns]
    stats = stats.rename(columns={'RingNbr_count': 'TotalPoomsae'})

    # Filter DataFrame
    filtered_df = stats if competition == 'All' else stats[stats['EventName'] == competition]
    filtered_df = filtered_df if referee == 'All' else filtered_df[filtered_df['RefereeName'] == referee]

    # Create a styled DataFrame with hidden index
    df_styled = filtered_df.style.hide(axis='index')

    # Create table
    table = pn.widgets.DataFrame(
        filtered_df, 
        show_index=False , 
        name='Summary Statistics', 
        sizing_mode='stretch_width'
    )

    return pn.Column(table)

#Builds the Event Table
with open('sql/RefereeAccPres.sql','r') as file:
    sql = file.read()
    file.close()

poomsaeprodb = 'PoomsaeProConnector/PoomsaePro.db'

df=load_data(poomsaeprodb, sql)

event_names = list(df['EventName'].unique())
event_names.sort()

referee_names = list(df["RefereeName"].unique())
referee_names.sort()

#Define Callback to update referee names list based on Competition
def update_referees(event):
    if event.new == 'All':
        referee_names = list(df["RefereeName"].unique())
    else:
        referee_names = list(df[df['EventName'] == event.new]["RefereeName"].unique())
    Referee_select.options = ['All'] + sorted(referee_names)

# Create Competition dropdown
Competition_select = pn.widgets.Select(
    name='Filter by Competition',
    options=['All'] + event_names,
    value='All'
)

# Create Referee dropdown
Referee_select = pn.widgets.Select(
    name="Filter by Referee",
    options=["All"] + referee_names,
    value="All"
)

# Create Event dropdown
Event_select = pn.widgets.Select(
    name='Filter by Event',
    options=['All','Recognized','Freestyle','Demo','Para','Mixed'],
    value='All'
)

# Bind dropdown to dashboard
dashboard = pn.bind(create_dashboard, 
                     event=Event_select, referee=Referee_select, competition = Competition_select,
                     db_path=poomsaeprodb, sql=sql)

#Bind the Call back
Competition_select.param.watch(update_referees, 'value')

# Layout
layout = pn.Column(
    pn.pane.Markdown("Poomsae Referee Analysis"),
    Competition_select,
    Event_select,
    Referee_select,
    dashboard
)

# Serve the dashboard
layout.servable()

#panel serve RefereeReportDashboard.py --show

