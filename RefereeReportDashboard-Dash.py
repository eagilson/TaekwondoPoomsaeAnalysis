import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

from utils import categorize_event, load_data

# Create table data
def create_table_data(db_path, sql_file_path, competition='All', event='All', referee='All'):
    df = load_data(db_path, sql_file_path)
    if df is None:
        return pd.DataFrame(), "Error: Failed to load data."

    # Categorize Division
    df['Division_category'] = df['Division'].apply(categorize_event)
    
    # Calculate differences
    df['AccDifference'] = df['Accuracy'] - df['TotalAccuracy']
    df['PresDifference'] = df['Presentation'] - df['TotalPresentation']

    # Event filter before grouping
    df = df if event == 'All' else df[df['Division_category'] == event]

    # Generate summary statistics grouped by name
    group_by = ['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName']
    stats = df.groupby(group_by).agg({
        'RingNbr': 'count',
        'AccDifference': ['mean', 'std'],
        'PresDifference': ['mean', 'std']
    }).reset_index()
    
    # Flatten the MultiIndex and rename the RingNbr count column
    stats.columns = ['_'.join(col).strip() if col[1] else col[0] for col in stats.columns]
    stats = stats.rename(columns={'RingNbr_count': 'TotalPoomsae'})

    # Filter DataFrame
    filtered_df = stats if competition == 'All' else stats[stats['EventName'] == competition]
    filtered_df = filtered_df if referee == 'All' else filtered_df[filtered_df['RefereeName'] == referee]

    return filtered_df, None


db_path = 'PoomsaeProConnector/PoomsaePro.db'
sql_file_path = 'sql/RefereeAccPres.sql'

# Load initial data for dropdown options
df = load_data(db_path, sql_file_path)
event_names = ['All'] + sorted(df['EventName'].unique()) if df is not None else ['All']
referee_names = ['All'] + sorted(df['RefereeName'].unique()) if df is not None else ['All']

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Poomsae Referee Analysis"),
    html.Label("Filter by Competition"),
    dcc.Dropdown(
        id='competition-select',
        options=[{'label': name, 'value': name} for name in event_names],
        value='All',
        style={'width': '50%'}
    ),
    html.Label("Filter by Event"),
    dcc.Dropdown(
        id='event-select',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Recognized', 'value': 'Recognized'},
            {'label': 'Freestyle', 'value': 'Freestyle'},
            {'label': 'Demo', 'value': 'Demo'},
            {'label': 'Para', 'value': 'Para'},
            {'label': 'Mixed', 'value': 'Mixed'}
        ],
        value='All',
        style={'width': '50%'}
    ),
    html.Label("Filter by Referee"),
    dcc.Dropdown(
        id='referee-select',
        options=[{'label': name, 'value': name} for name in referee_names],
        value='All',
        style={'width': '50%'}
    ),
    dash_table.DataTable(
        id='summary-table',
        columns=[],
        data=[],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
    ),
    html.Div(id='error-message')
])

# Callback to update referee dropdown based on competition
@app.callback(
    Output('referee-select', 'options'),
    Input('competition-select', 'value')
)
def update_referees(competition):
    if df is None:
        return [{'label': 'All', 'value': 'All'}]
    if competition == 'All':
        referee_names = sorted(df['RefereeName'].unique())
    else:
        referee_names = sorted(df[df['EventName'] == competition]['RefereeName'].unique())
    return [{'label': 'All', 'value': 'All'}] + [{'label': name, 'value': name} for name in referee_names]

# Callback to update table
@app.callback(
    [Output('summary-table', 'columns'),
     Output('summary-table', 'data'),
     Output('error-message', 'children')],
    [Input('competition-select', 'value'),
     Input('event-select', 'value'),
     Input('referee-select', 'value')]
)
def update_table(competition, event, referee):
    filtered_df, error = create_table_data(db_path, sql_file_path, competition, event, referee)
    
    if error:
        return [], [], error
    
    columns = [{'name': col, 'id': col} for col in filtered_df.columns]
    data = filtered_df.to_dict('records')
    
    return columns, data, ""

# Run the app
if __name__ == '__main__':
    app.run(debug=True)