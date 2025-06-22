import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from utils import load_data, categorize_event, categorize_belt
import numpy as np

# Load data
db_path = 'PoomsaeProConnector/PoomsaePro.db'
sql_file_path = 'sql/RefereeFullScore.sql'
df = load_data(db_path, sql_file_path)

if df is None or df.empty:
    raise Exception("Failed to load data from database or no data returned.")

# Reset index to ensure uniqueness
df = df.reset_index(drop=True)

# Convert score, average, placement, and order columns to numeric, coercing errors to NaN
# Do NOT convert Round to numeric
for form in ['A', 'B', 'T']:
    df[f'Accuracy_{form}'] = pd.to_numeric(df[f'Accuracy_{form}'], errors='coerce')
    df[f'Presentation_{form}'] = pd.to_numeric(df[f'Presentation_{form}'], errors='coerce')
    df[f'Acc_Avg_{form}'] = pd.to_numeric(df[f'Acc_Avg_{form}'], errors='coerce')
    df[f'Pre_Avg_{form}'] = pd.to_numeric(df[f'Pre_Avg_{form}'], errors='coerce')
df['Placement'] = pd.to_numeric(df['Placement'], errors='coerce')
df['Round_ID'] = pd.to_numeric(df['Round_ID'], errors='coerce')
df['OrderOfPerform'] = pd.to_numeric(df['OrderOfPerform'], errors='coerce')

# Add Belt column using categorize_belt
df['Belt'] = df['Category'].apply(categorize_belt)

# Compute Official Placement based on simplified rule, only for Round_ID >= 9
def compute_official_placement(df):
    df['Official_Placement'] = df['Placement'].copy()
    # Apply rules only for single-elimination rounds (Round_ID >= 9)
    single_elim_mask = df['Round_ID'] >= 9
    df.loc[single_elim_mask & (df['Placement'] == 0), 'Official_Placement'] = 1
    df.loc[single_elim_mask & (df['Placement'] > 2), 'Official_Placement'] = 2
    return df

# Compute Referee_Placement
def compute_referee_placement(group):
    # Initialize columns for ranking metrics
    group['Avg_Acc_Pres_AB'] = np.nan
    group['Avg_Pres_AB'] = np.nan
    group['Acc_Pres_T'] = np.nan
    group['Ranking_Score'] = np.nan

    # Calculate metrics for each performance
    for idx in group.index:
        acc_a = group.at[idx, 'Accuracy_A']
        pre_a = group.at[idx, 'Presentation_A']
        form_b = group.at[idx, 'FormName_B']
        acc_b = group.at[idx, 'Accuracy_B']
        pre_b = group.at[idx, 'Presentation_B']
        acc_t = group.at[idx, 'Accuracy_T']
        pre_t = group.at[idx, 'Presentation_T']

        # Primary metric: Average of Acc+Pres for A and B (if B is valid)
        if pd.notna(acc_a) and pd.notna(pre_a) and acc_a != -1 and pre_a != -1:
            ab_scores = [acc_a + pre_a]
            if form_b not in [None, 'None', ''] and pd.notna(acc_b) and pd.notna(pre_b) and acc_b != -1 and pre_b != -1:
                ab_scores.append(acc_b + pre_b)
            group.at[idx, 'Avg_Acc_Pres_AB'] = np.mean(ab_scores)
        
        # Tiebreaker 1: Average of Presentation for A and B (if B is valid)
        if pd.notna(pre_a) and pre_a != -1:
            pres_scores = [pre_a]
            if form_b not in [None, 'None', ''] and pd.notna(pre_b) and pre_b != -1:
                pres_scores.append(pre_b)
            group.at[idx, 'Avg_Pres_AB'] = np.mean(pres_scores)
        
        # Tiebreaker 2: Acc+Pres for T (if T is valid)
        if (group.at[idx, 'FormName_T'] not in [None, 'None', '']) and pd.notna(acc_t) and pd.notna(pre_t) and acc_t != -1 and pre_t != -1:
            group.at[idx, 'Acc_Pres_T'] = acc_t + pre_t

        # Compute Ranking_Score
        avg_acc_pres_ab = group.at[idx, 'Avg_Acc_Pres_AB']
        avg_pres_ab = group.at[idx, 'Avg_Pres_AB']
        acc_pres_t = group.at[idx, 'Acc_Pres_T']
        ranking_score = 0
        if pd.notna(avg_acc_pres_ab):
            ranking_score += avg_acc_pres_ab
        if pd.notna(avg_pres_ab):
            ranking_score += avg_pres_ab / 10**3
        if pd.notna(acc_pres_t):
            ranking_score += acc_pres_t / 10**6
        group.at[idx, 'Ranking_Score'] = ranking_score if ranking_score != 0 else np.nan

    # Rank performances
    if group['Round_ID'].iloc[0] >= 9:
        # Single-elimination: pair athletes by OrderOfPerform summing to target_sum
        round_id = group['Round_ID'].iloc[0]
        round_size = 2 ** (7 - (round_id - 9))
        target_sum = round_size + 1
        group['Referee_Placement'] = np.nan

        # Find pairs where OrderOfPerform sums to target_sum
        for i, row1 in group.iterrows():
            order1 = row1['OrderOfPerform']
            if pd.isna(order1):
                continue
            # Look for a matching athlete
            match = group[
                (group['OrderOfPerform'] == target_sum - order1) &
                (group.index != i)
            ]
            if not match.empty:
                row2 = match.iloc[0]
                # Compare metrics
                metrics1 = (
                    row1['Avg_Acc_Pres_AB'] or -np.inf,
                    row1['Avg_Pres_AB'] or -np.inf,
                    row1['Acc_Pres_T'] or -np.inf
                )
                metrics2 = (
                    row2['Avg_Acc_Pres_AB'] or -np.inf,
                    row2['Avg_Pres_AB'] or -np.inf,
                    row2['Acc_Pres_T'] or -np.inf
                )
                # Rank 1 for higher, 2 for lower, 1.5 for ties
                if metrics1 > metrics2:
                    group.at[i, 'Referee_Placement'] = 1
                    group.at[row2.name, 'Referee_Placement'] = 2
                elif metrics1 < metrics2:
                    group.at[i, 'Referee_Placement'] = 2
                    group.at[row2.name, 'Referee_Placement'] = 1
                else:
                    group.at[i, 'Referee_Placement'] = 1.5
                    group.at[row2.name, 'Referee_Placement'] = 1.5
    else:
        # Non-single-elimination: rank all athletes by Ranking_Score
        if group['Ranking_Score'].notna().any():
            group['Referee_Placement'] = group['Ranking_Score'].rank(
                method='average', ascending=False, na_option='bottom'
            )
        else:
            group['Referee_Placement'] = np.nan

    return group[['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName', 'Performance_ID', 'Referee_Placement', 'Ranking_Score']]

# Apply Official Placement computation
df = compute_official_placement(df)
df['Placement'] = df['Official_Placement']
df = df.drop(columns=['Official_Placement'])

# Apply Referee_Placement computation
placement_df = df.groupby(['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName']).apply(compute_referee_placement).reset_index(drop=True)
df = df.merge(placement_df, on=['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName', 'Performance_ID'])

# Renormalize Placement and Referee_Placement
def normalize_ranks(group):
    # Check Round_ID for the group
    round_id = group['Round_ID'].iloc[0]
    if round_id >= 9:
        # For single-elimination rounds, use rank - 1
        group['Placement'] = group['Placement'] - 1
        group['Referee_Placement'] = group['Referee_Placement'] - 1
    else:
        # For non-single-elimination rounds, use (rank - 1) / (n - 1)
        n = group['Performance_ID'].nunique()
        if n > 1:
            group['Placement'] = (group['Placement'] - 1) / (n - 1)
            group['Referee_Placement'] = (group['Referee_Placement'] - 1) / (n - 1)
        else:
            # If n=1, set to 0 (highest rank)
            group['Placement'] = 0
            group['Referee_Placement'] = 0
    return group

# Apply normalization within each group
df = df.groupby(['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName']).apply(normalize_ranks).reset_index(drop=True)

# Compute difference columns for Accuracy and Presentation
for form in ['A', 'B', 'T']:
    df[f'Acc_Diff_{form}'] = df[f'Accuracy_{form}'] - df[f'Acc_Avg_{form}']
    df[f'Pre_Diff_{form}'] = df[f'Presentation_{form}'] - df[f'Pre_Avg_{form}']

# Preprocess data
df['Event_Category'] = df['Division'].apply(categorize_event)

# Compute referee scores (combine Accuracy and Presentation for each form)
def compute_referee_score(row):
    score = 0
    count = 0
    for form in ['A', 'B', 'T']:
        if row[f'FormName_{form}'] not in [None, 'None', '']:
            acc = row[f'Accuracy_{form}']
            pre = row[f'Presentation_{form}']
            if pd.notna(acc) and pd.notna(pre) and acc != -1 and pre != -1:
                score += acc + pre
                count += 1
    return score / count if count > 0 else None

# Apply referee score calculation
df['Referee_Score'] = df.apply(compute_referee_score, axis=1)

# Compute summary statistics
def compute_stats(group):
    # Initialize lists for valid differences
    pre_diffs = []
    acc_diffs = []
    
    # Filter rows for each form based on valid FormName and non -1 scores
    for form in ['A', 'B', 'T']:
        valid_rows = group[
            (group[f'FormName_{form}'].notna()) & 
            (group[f'FormName_{form}'] != 'None') & 
            (group[f'FormName_{form}'] != '') & 
            (group[f'Accuracy_{form}'] != -1) & 
            (group[f'Presentation_{form}'] != -1)
        ]
        if not valid_rows.empty:
            # Extract differences where scores are valid
            pre_diff = valid_rows[f'Pre_Diff_{form}']
            acc_diff = valid_rows[f'Acc_Diff_{form}']
            if not pre_diff.empty and pre_diff.notna().any():
                pre_diffs.extend(pre_diff[pre_diff.notna()])
            if not acc_diff.empty and acc_diff.notna().any():
                acc_diffs.extend(acc_diff[acc_diff.notna()])
    
    # Convert to Series for computation
    pre_diffs = pd.Series(pre_diffs)
    acc_diffs = pd.Series(acc_diffs)
    
    stats = {
        'Athletes': group['Performance_ID'].nunique(),
        'Presentation_Diff_SD': pre_diffs.std() if not pre_diffs.empty else np.nan,
        'Accuracy_Diff_SD': acc_diffs.std() if not acc_diffs.empty else np.nan,
        'Presentation_Diff_Mean': pre_diffs.mean() if not pre_diffs.empty else np.nan,
        'Accuracy_Diff_Mean': acc_diffs.mean() if not acc_diffs.empty else np.nan,
    }
    # Compute correlation between normalized referee placement and placement
    valid_rows = group[['Referee_Placement', 'Placement']].dropna()
    if len(valid_rows) > 1:
        stats['Correlation'] = valid_rows['Referee_Placement'].corr(valid_rows['Placement'])
    else:
        stats['Correlation'] = np.nan
    return pd.Series(stats)

# Group by RefereeName, EventName, Event_Category, and Belt
stats_df = df.groupby(['RefereeName', 'EventName', 'Event_Category', 'Belt']).apply(compute_stats, include_groups=False).reset_index()

# Round numeric columns for display to 3 decimal places
numeric_cols = ['Correlation', 'Presentation_Diff_SD', 'Accuracy_Diff_SD', 'Presentation_Diff_Mean', 'Accuracy_Diff_Mean']
stats_df[numeric_cols] = stats_df[numeric_cols].round(3)
stats_df[numeric_cols] = stats_df[numeric_cols].fillna('-')  # Replace NaN with '-'

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Referee Scoring Performance Dashboard"),
    html.Div([
        html.Label("Event:"),
        dcc.Dropdown(
            id='event-filter',
            options=[{'label': event, 'value': event} for event in sorted(df['EventName'].unique())],
            value=None,
            multi=True,
            placeholder="Select Event(s)"
        ),
    ], style={'marginBottom': 20, 'width': '30%'}),
    html.Div([
        html.Label("Referee Name:"),
        dcc.Dropdown(
            id='referee-filter',
            options=[{'label': name, 'value': name} for name in sorted(df['RefereeName'].unique())],
            value=None,
            multi=True,
            placeholder="Select Referee(s)"
        ),
    ], style={'marginBottom': 20, 'width': '30%'}),
    html.Div([
        html.Label("Event Category:"),
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': cat, 'value': cat} for cat in sorted(df['Event_Category'].unique())],
            value=None,
            multi=False,
            placeholder="Select Event Category"
        ),
    ], style={'marginBottom': 20, 'width': '30%'}),
    html.Div([
        html.Label("Belt:"),
        dcc.Dropdown(
            id='belt-filter',
            options=[{'label': belt, 'value': belt} for belt in sorted(df['Belt'].unique())],
            value=None,
            multi=True,
            placeholder="Select Belt(s)"
        ),
    ], style={'marginBottom': 20, 'width': '30%'}),
    dcc.Loading(
        id="loading",
        type="circle",
        children=[
            dash_table.DataTable(
                id='stats-table',
                columns=[
                    {'name': 'Referee Name', 'id': 'RefereeName'},
                    {'name': 'Event', 'id': 'EventName'},
                    {'name': 'Event Category', 'id': 'Event_Category'},
                    {'name': 'Athletes', 'id': 'Athletes'},
                    {'name': 'Correlation', 'id': 'Correlation'},
                    {'name': 'Presentation Diff SD', 'id': 'Presentation_Diff_SD'},
                    {'name': 'Accuracy Diff SD', 'id': 'Accuracy_Diff_SD'},
                    {'name': 'Presentation Diff Mean', 'id': 'Presentation_Diff_Mean'},
                    {'name': 'Accuracy Diff Mean', 'id': 'Accuracy_Diff_Mean'},
                ],
                data=stats_df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px', 'minWidth': '100px', 'maxWidth': '200px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'},
                page_size=10,
                sort_action='native',
                filter_action='native',
            )
        ]
    )
])

# Callback to update referee dropdown based on selected events
@app.callback(
    Output('referee-filter', 'options'),
    Input('event-filter', 'value')
)
def update_referee_options(selected_events):
    if not selected_events:
        return [{'label': name, 'value': name} for name in sorted(df['RefereeName'].unique())]
    filtered_df = df[df['EventName'].isin(selected_events)]
    return [{'label': name, 'value': name} for name in sorted(filtered_df['RefereeName'].unique())]

# Callback to update table based on filters
@app.callback(
    Output('stats-table', 'data'),
    [
        Input('referee-filter', 'value'),
        Input('event-filter', 'value'),
        Input('category-filter', 'value'),
        Input('belt-filter', 'value')
    ]
)
def update_table(referee, event, category, belt):
    filtered_df = stats_df
    if referee:
        filtered_df = filtered_df[filtered_df['RefereeName'].isin(referee)]
    if event:
        filtered_df = filtered_df[filtered_df['EventName'].isin(event)]
    if category:
        filtered_df = filtered_df[filtered_df['Event_Category'] == category]
    if belt:
        filtered_df = filtered_df[filtered_df['Belt'].isin(belt)]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)