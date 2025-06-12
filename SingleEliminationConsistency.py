import pandas as pd
import statsmodels.stats.inter_rater as ir
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
from utils import categorize_event, load_data, categorize_division

# Compute referee ratings with tiebreakers
def compute_referee_ratings(row_a, row_b, referee):
    score_a = row_a[f'Acc_{referee}_A'] + row_a[f'Pre_{referee}_A'] + row_a[f'Acc_{referee}_B'] + row_a[f'Pre_{referee}_B']
    score_b = row_b[f'Acc_{referee}_A'] + row_b[f'Pre_{referee}_A'] + row_b[f'Acc_{referee}_B'] + row_b[f'Pre_{referee}_B']
    if score_a > score_b:
        return 1  # Chung (A)
    elif score_a < score_b:
        return 0  # Hong (B)
    # Tiebreaker 1: Presentation sum
    pres_a = row_a[f'Pre_{referee}_A'] + row_a[f'Pre_{referee}_B']
    pres_b = row_b[f'Pre_{referee}_A'] + row_b[f'Pre_{referee}_B']
    if pres_a > pres_b:
        return 1
    elif pres_a < pres_b:
        return 0
    # Tiebreaker 2: Tiebreaker form (if contested)
    if row_a['TieBreaker_Score'] > -1:
        tie_a = row_a[f'Acc_{referee}_T'] + row_a[f'Pre_{referee}_T']
        tie_b = row_b[f'Acc_{referee}_T'] + row_b[f'Pre_{referee}_T']
        if tie_a > tie_b:
            return 1
        elif tie_a < tie_b:
            return 0
    return 2  # Tie

# Compute final result with tiebreakers (no ties allowed)
def compute_final_result(row_a, row_b):
    score_a = row_a['Form_Score_AB']
    score_b = row_b['Form_Score_AB']
    if score_a > score_b:
        return 1  # Chung (A)
    elif score_a < score_b:
        return 0  # Hong (B)
    # Tiebreaker 1: Presentation_Total
    pres_a = row_a['Presentation_Total']
    pres_b = row_b['Presentation_Total']
    if pres_a > pres_b:
        return 1
    elif pres_a < pres_b:
        return 0
    # Tiebreaker 2: Full_Score
    full_a = row_a['Full_Score']
    full_b = row_b['Full_Score']
    if full_a > full_b:
        return 1
    elif full_a < full_b:
        return 0
    # Tiebreaker 3: Tiebreaker form (if contested)
    if row_a['TieBreaker_Score'] > -1:
        tie_a = row_a['Acc_Avg_T'] + row_a['Pre_Avg_T']
        tie_b = row_b['Acc_Avg_T'] + row_b['Pre_Avg_T']
        if tie_a > tie_b:
            return 1
        elif tie_a < tie_b:
            return 0
    # Tiebreaker 4: TieBreaker_Total
    tie_total_a = row_a['TieBreaker_Total']
    tie_total_b = row_b['TieBreaker_Total']
    if tie_total_a > tie_total_b:
        return 1
    elif tie_total_a < tie_total_b:
        return 0
    return 0  # Default to Hong (B) for unresolved cases, as ties are not allowed

# Pair athletes, assigning Chung to odd OrderOfPerform
def pair_athletes(df):
    paired_data = []
    for round_id in df['Round_ID'].unique():
        round_size = 2 ** (7 - (round_id - 9))
        target_sum = round_size + 1
        round_df = df[df['Round_ID'] == round_id].copy()
        round_df = round_df.sort_values('OrderOfPerform')
        for i in range(len(round_df) // 2):
            row_a = round_df.iloc[i]
            row_b = round_df.iloc[len(round_df) - 1 - i]
            if row_a['OrderOfPerform'] + row_b['OrderOfPerform'] == target_sum:
                # Assign Chung (A) to the athlete with odd OrderOfPerform
                if row_a['OrderOfPerform'] % 2 == 1:
                    chung_row, hong_row = row_a, row_b
                else:
                    chung_row, hong_row = row_b, row_a
                ratings = pd.Series([compute_referee_ratings(chung_row, hong_row, ref) for ref in ['R', 'J1', 'J2', 'J3', 'J4']],
                                   index=['referee1', 'referee2', 'referee3', 'referee4', 'referee5'])
                final_result = compute_final_result(chung_row, hong_row)
                paired_data.append({
                    'EventName': chung_row['EventName'],
                    'Division': chung_row['Division'],
                    'DivisionCategory': chung_row['DivisionCategory'],
                    'Round_ID': round_id,
                    'Round_Name': f"Round of {round_size}",
                    'OrderOfPerform_A': chung_row['OrderOfPerform'],
                    'OrderOfPerform_B': hong_row['OrderOfPerform'],
                    'Competitor_A': chung_row['CompetitorNbr'],
                    'Competitor_B': hong_row['CompetitorNbr'],
                    'referee1': ratings['referee1'],
                    'referee2': ratings['referee2'],
                    'referee3': ratings['referee3'],
                    'referee4': ratings['referee4'],
                    'referee5': ratings['referee5'],
                    'Final_Result': final_result
                })
    return pd.DataFrame(paired_data)

# Interpret Fleiss' Kappa
def interpret_kappa(kappa):
    if kappa <= 0:
        return "No agreement (or worse than chance): Referees' ratings are highly inconsistent, possibly due to differing interpretations of Poomsae scoring criteria."
    elif 0.01 <= kappa <= 0.20:
        return "Slight agreement: Minimal consistency beyond chance, indicating significant variability in referee judgments. Clearer scoring guidelines may be needed."
    elif 0.21 <= kappa <= 0.40:
        return "Fair agreement: Some consistency, but notable disagreement persists. This may reflect subjective differences in judging Chung vs. Hong, including frequent ties."
    elif 0.41 <= kappa <= 0.60:
        return "Moderate agreement: Reasonable consistency among referees, with some discrepancies suggesting potential for improved training or standardization."
    elif 0.61 <= kappa <= 0.80:
        return "Substantial agreement: Strong consistency in referee ratings, indicating reliable scoring for Chung vs. Hong."
    else:
        return "Almost perfect agreement: Near-unanimous ratings, suggesting highly consistent referee judgments due to clear criteria and training."

# Load data
db_path = 'PoomsaeProConnector/PoomsaePro.db'
sql_file_path = 'sql/RefereeScoresSingleElimination.sql'
df = load_data(db_path, sql_file_path)
if df is None:
    raise Exception("Failed to load data")

# Add categorizations
df['EventCategory'] = df['EventName'].apply(categorize_event)
df['DivisionCategory'] = df['Division'].apply(categorize_division)

# Process data
paired_df = pair_athletes(df)

# Calculate metrics
def calculate_metrics(df_subset):
    if df_subset.empty:
        return None, None, None, "No data available for selected events or divisions."
    
    # Three categories: 0 (Hong), 1 (Chung), 2 (Tie)
    fleiss_data = [[sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 0),
                    sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 1),
                    sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 2)]
                   for _, row in df_subset.iterrows()]
    try:
        kappa = ir.fleiss_kappa(fleiss_data)
    except:
        return None, None, None, "Cannot compute Kappa: insufficient or uniform ratings."
    
    n_pairs = len(df_subset)
    n_referees = 5
    total_ratings = n_pairs * n_referees
    P_bar = df_subset.apply(lambda row: (sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 0) * 
                                        (sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 0) - 1) + 
                                        sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 1) * 
                                        (sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 1) - 1) +
                                        sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 2) * 
                                        (sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 2) - 1)) / 
                                        (n_referees * (n_referees - 1)), axis=1).mean()
    total_0s = sum(row[0] for row in fleiss_data)
    total_1s = sum(row[1] for row in fleiss_data)
    total_2s = sum(row[2] for row in fleiss_data)
    p0 = total_0s / total_ratings
    p1 = total_1s / total_ratings
    p2 = total_2s / total_ratings
    P_e = p0**2 + p1**2 + p2**2
    kappa_interpretation = interpret_kappa(kappa)
    return kappa, P_bar, P_e, kappa_interpretation

# Initial metrics
kappa, P_bar, P_e, kappa_interpretation = calculate_metrics(paired_df)

# Dash Dashboard
app = dash.Dash(__name__)

# Dropdown options
event_options = [{'label': event, 'value': event} for event in sorted(paired_df['EventName'].unique())]
division_options = [{'label': div, 'value': div} for div in sorted(paired_df['DivisionCategory'].unique())]

app.layout = html.Div([
    html.H1("Taekwondo Poomsae Referee Agreement Dashboard"),
    html.Label("Select Event(s):"),
    dcc.Dropdown(
        id='event-filter',
        options=event_options,
        value=None,  # Default: all events
        multi=True,
        placeholder="Select one or more events..."
    ),
    html.Label("Select Division Category(s):", style={'marginTop': '10px'}),
    dcc.Dropdown(
        id='division-filter',
        options=division_options,
        value=None,  # Default: all divisions
        multi=True,
        placeholder="Select one or more division categories..."
    ),
    html.H3(id='kappa-display', children=f"Fleiss' Kappa: {kappa:.3f}" if kappa is not None else "Fleiss' Kappa: N/A"),
    html.H4(id='kappa-interpretation', children=f"Interpretation: {kappa_interpretation}"),
    html.H4(id='observed-agreement', children=f"Observed Agreement: {P_bar:.3f}" if P_bar is not None else "Observed Agreement: N/A"),
    html.H4(id='expected-agreement', children=f"Expected Agreement: {P_e:.3f}" if P_e is not None else "Expected Agreement: N/A"),
    html.P("The chart below compares observed and expected agreement among referees for Chung vs. Hong ratings, including ties."),
    dcc.Graph(id='agreement-chart')
])

# Callback to update metrics and chart
@app.callback(
    [Output('kappa-display', 'children'),
     Output('kappa-interpretation', 'children'),
     Output('observed-agreement', 'children'),
     Output('expected-agreement', 'children'),
     Output('agreement-chart', 'figure')],
    [Input('event-filter', 'value'),
     Input('division-filter', 'value')]
)
def update_dashboard(selected_events, selected_divisions):
    df_subset = paired_df
    if selected_events:
        df_subset = df_subset[df_subset['EventName'].isin(selected_events)]
    if selected_divisions:
        df_subset = df_subset[df_subset['DivisionCategory'].isin(selected_divisions)]
    
    kappa, P_bar, P_e, kappa_interpretation = calculate_metrics(df_subset)
    
    chart_data = pd.DataFrame({
        'Metric': ['Observed Agreement', 'Expected Agreement'],
        'Value': [P_bar if P_bar is not None else 0, P_e if P_e is not None else 0]
    })
    
    fig = px.bar(chart_data, x='Metric', y='Value',
                 title="Observed vs. Expected Agreement",
                 color='Metric', color_discrete_map={'Observed Agreement': '#1f77b4', 'Expected Agreement': '#ff7f0e'})
    
    return (
        f"Fleiss' Kappa: {kappa:.3f}" if kappa is not None else "Fleiss' Kappa: N/A",
        f"Interpretation: {kappa_interpretation}",
        f"Observed Agreement: {P_bar:.3f}" if P_bar is not None else "Observed Agreement: N/A",
        f"Expected Agreement: {P_e:.3f}" if P_e is not None else "Expected Agreement: N/A",
        fig
    )

if __name__ == '__main__':
    app.run(debug=True)