import pandas as pd
import statsmodels.stats.inter_rater as ir
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
from utils.PoomsaeProCleaning import categorize_event, load_data, categorize_division, extract_age, categorize_belt
from scipy.stats import norm

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

# Pair athletes within EventName, Division, Gender, Category, and Round_ID
def pair_athletes(df):
    if df is None or not isinstance(df, pd.DataFrame):
        print("Error: Input DataFrame is None or invalid")
        return pd.DataFrame()

    required_columns = ['EventName', 'Division', 'DivisionAge', 'Gender', 'Category', 'Round_ID', 'OrderOfPerform', 'CompetitorNbr']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing required columns in input DataFrame: {', '.join(missing_columns)}")
        return pd.DataFrame()

    paired_data = []
    for (event_name, division, gender, category, round_id), group_df in df.groupby(['EventName', 'Division', 'Gender', 'Category', 'Round_ID']):
        round_size = 2 ** (7 - (round_id - 9))
        target_sum = round_size + 1
        round_df = group_df.sort_values('OrderOfPerform')
        if len(round_df) > round_size:
            print(f"Warning: Group {event_name}, {division}, {gender}, {category}, Round_ID {round_id} has {len(round_df)} athletes, exceeding max {round_size}")
        for _, row_a in round_df.iterrows():
            order_a = row_a['OrderOfPerform']
            order_b = target_sum - order_a
            row_b_candidates = round_df[round_df['OrderOfPerform'] == order_b]
            if not row_b_candidates.empty:
                row_b = row_b_candidates.iloc[0]
                if row_a['CompetitorNbr'] != row_b['CompetitorNbr'] and order_a < order_b:
                    if row_a['OrderOfPerform'] % 2 == 1:
                        chung_row, hong_row = row_a, row_b
                    else:
                        chung_row, hong_row = row_b, row_a
                    ratings = pd.Series(
                        [compute_referee_ratings(chung_row, hong_row, ref) for ref in ['R', 'J1', 'J2', 'J3', 'J4']],
                        index=['referee1', 'referee2', 'referee3', 'referee4', 'referee5']
                    )
                    final_result = compute_final_result(chung_row, hong_row)
                    paired_data.append({
                        'EventName': chung_row['EventName'],
                        'EventCategory': chung_row['EventCategory'],
                        'Division': chung_row['Division'],
                        'DivisionAge': chung_row['DivisionAge'],
                        'DivisionCategory': chung_row['DivisionCategory'],
                        'Gender': chung_row['Gender'],
                        'Category': chung_row['Category'],
                        'Belt': chung_row['Belt'],
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

def calculate_metrics(df_subset):
    empty_outcomes = pd.DataFrame({'Outcome': [], 'Count': []})
    if df_subset is None or not isinstance(df_subset, pd.DataFrame) or df_subset.empty:
        return None, None, None, None, None, empty_outcomes, "No data available for selected events or divisions."

    fleiss_data = [[sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 0),
                    sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 1),
                    sum(row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']] == 2)]
                   for _, row in df_subset.iterrows()]
    try:
        kappa = ir.fleiss_kappa(fleiss_data)
    except Exception as e:
        print(f"Error computing Fleiss' Kappa: {str(e)}")
        return None, None, None, None, None, empty_outcomes, "Cannot compute Kappa: insufficient or uniform ratings."

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

    p_j = [p0, p1, p2]
    se_numerator = P_bar + P_e - 2 * sum(p_j[j] * p_j[j] * P_bar for j in range(3)) - P_e**2
    se_denominator = (1 - P_e)**2 * n_referees * n_pairs
    se_kappa = (se_numerator / se_denominator)**0.5 if se_denominator != 0 else float('inf')

    z_score = kappa / se_kappa if se_kappa != 0 else float('inf')
    p_value = 2 * (1 - norm.cdf(abs(z_score))) if z_score != float('inf') else 0.0

    outcomes = []
    for _, row in df_subset.iterrows():
        votes = row[['referee1', 'referee2', 'referee3', 'referee4', 'referee5']].values
        winner = row['Final_Result']
        loser = 1 - winner
        agree_count = sum(votes == winner)
        disagree_count = sum(votes == loser)
        tie_count = sum(votes == 2)
        outcomes.append(f"{agree_count}-{disagree_count}-{tie_count}")

    outcome_counts = pd.Series(outcomes).value_counts()
    outcome_df = pd.DataFrame({
        'Outcome': outcome_counts.index,
        'Count': outcome_counts.values
    })
    outcome_df['Wins'] = outcome_df['Outcome'].apply(lambda x: int(x.split('-')[0]))
    outcome_df['Ties'] = outcome_df['Outcome'].apply(lambda x: int(x.split('-')[2]))
    outcome_df = outcome_df.sort_values(by=['Wins', 'Ties'], ascending=[False, False])
    outcome_df = outcome_df[['Outcome', 'Count']]

    return kappa, P_bar, P_e, z_score, p_value, outcome_df, interpret_kappa(kappa)

def apply_filters(df, selected_event_types=None, selected_events=None, selected_division_categories=None,
                  selected_division_ages=None, selected_belts=None, selected_rounds=None):
    df_subset = df if isinstance(df, pd.DataFrame) else pd.DataFrame()
    if selected_event_types:
        df_subset = df_subset[df_subset['EventCategory'].isin(selected_event_types)]
    if selected_events:
        df_subset = df_subset[df_subset['EventName'].isin(selected_events)]
    if selected_division_categories:
        df_subset = df_subset[df_subset['DivisionCategory'].isin(selected_division_categories)]
    if selected_division_ages:
        df_subset = df_subset[df_subset['DivisionAge'].isin(selected_division_ages)]
    if selected_belts:
        df_subset = df_subset[df_subset['Belt'].isin(selected_belts)]
    if selected_rounds:
        df_subset = df_subset[df_subset['Round_Name'].isin(selected_rounds)]
    return df_subset

# Load data
db_path = 'PoomsaeProConnector/PoomsaePro.db'
sql_file_path = 'sql/RefereeScoresSingleElimination.sql'
df = load_data(db_path, sql_file_path)
if df is None or not isinstance(df, pd.DataFrame):
    print("Error: Failed to load data from database")
    df = pd.DataFrame()

if not df.empty:
    df['EventCategory'] = df['EventName'].apply(categorize_event)
    df['DivisionCategory'] = df['Division'].apply(categorize_division)
    df['DivisionAge'] = df['Division'].apply(extract_age)
    df['Belt'] = df['Category'].apply(categorize_belt)
else:
    print("Warning: No data loaded; proceeding with empty DataFrame")

paired_df = pair_athletes(df)
if paired_df is None or not isinstance(paired_df, pd.DataFrame):
    print("Error: pair_athletes returned None or invalid DataFrame")
    paired_df = pd.DataFrame()

kappa, P_bar, P_e, z_score, p_value, outcome_df, kappa_interpretation = calculate_metrics(paired_df)

app = dash.Dash(__name__)

event_type_order = ['Recognized', 'Freestyle', 'Traditional', 'Mixed', 'Para', 'Demo']
event_type_options = []
if not paired_df.empty and 'EventCategory' in paired_df.columns:
    present_types = set(paired_df['EventCategory'].dropna().unique())
    event_type_options = [{'label': t, 'value': t} for t in event_type_order if t in present_types]
    event_type_options += [{'label': t, 'value': t} for t in sorted(present_types) if t not in event_type_order]
division_category_options = [{'label': div, 'value': div} for div in sorted(paired_df['DivisionCategory'].unique())] if not paired_df.empty else []

app.layout = html.Div([
    html.H1("Taekwondo Poomsae Referee Agreement Dashboard"),
    html.Label("Select Event Type(s):"),
    dcc.Dropdown(
        id='event-type-filter',
        options=event_type_options,
        value=None,
        multi=True,
        placeholder="Select one or more event types..."
    ),
    html.Label("Select Event(s):", style={'marginTop': '10px'}),
    dcc.Dropdown(
        id='event-filter',
        options=[],
        value=None,
        multi=True,
        placeholder="Select one or more events..."
    ),
    html.Label("Select Division Category(s):", style={'marginTop': '10px'}),
    dcc.Dropdown(
        id='division-filter',
        options=division_category_options,
        value=None,
        multi=True,
        placeholder="Select one or more division categories..."
    ),
    html.Label("Select Division(s):", style={'marginTop': '10px'}),
    dcc.Dropdown(
        id='division-selection',
        options=[],
        value=None,
        multi=True,
        placeholder="Select one or more divisions..."
    ),
    html.Label("Select Belt(s):", style={'marginTop': '10px'}),
    dcc.Dropdown(
        id='belt-filter',
        options=[],
        value=None,
        multi=True,
        placeholder="Select one or more belts..."
    ),
    html.Label("Select Round Name(s):", style={'marginTop': '10px'}),
    dcc.Dropdown(
        id='round-filter',
        options=[],
        value=None,
        multi=True,
        placeholder="Select one or more rounds..."
    ),
    html.H3(id='kappa-display', children=f"Fleiss' Kappa: {kappa:.3f}" if kappa is not None else "Fleiss' Kappa: N/A"),
    html.H4(id='kappa-interpretation', children=f"Interpretation: {kappa_interpretation}"),
    html.H4(id='observed-agreement', children=f"Observed Agreement: {P_bar:.3f}" if P_bar is not None else "Observed Agreement: N/A"),
    html.H4(id='expected-agreement', children=f"Expected Agreement: {P_e:.3f}" if P_e is not None else "Expected Agreement: N/A"),
    html.H4(id='z-score', children=f"Z-Score: {z_score:.3f}" if z_score is not None and z_score != float('inf') else "Z-Score: N/A"),
    html.H4(id='p-value', children=f"P-Value: {p_value:.4f}" if p_value is not None else "P-Value: N/A"),
    html.P("The chart below compares observed and expected agreement among referees for Chung vs. Hong ratings, including ties."),
    dcc.Graph(id='agreement-chart'),
    html.P("The pie chart below shows the distribution of match outcomes (X-Y-Z: referees agreeing with winner, disagreeing, and tying) based on Final_Result, ordered by wins then ties."),
    dcc.Graph(id='outcome-pie-chart')
])

@app.callback(
    Output('event-filter', 'options'),
    [Input('event-type-filter', 'value')]
)
def update_event_options(selected_event_types):
    df_subset = apply_filters(paired_df, selected_event_types=selected_event_types)
    if df_subset.empty or 'EventName' not in df_subset.columns:
        return []
    return [{'label': event, 'value': event} for event in sorted(df_subset['EventName'].dropna().unique())]

@app.callback(
    Output('division-selection', 'options'),
    [Input('event-type-filter', 'value'),
     Input('event-filter', 'value'),
     Input('division-filter', 'value')]
)
def update_division_age_options(selected_event_types, selected_events, selected_division_categories):
    df_subset = apply_filters(paired_df, selected_event_types, selected_events, selected_division_categories)
    if df_subset.empty or 'DivisionAge' not in df_subset.columns:
        return []
    return [{'label': div, 'value': div} for div in sorted(df_subset['DivisionAge'].dropna().unique())]

@app.callback(
    Output('belt-filter', 'options'),
    [Input('event-type-filter', 'value'),
     Input('event-filter', 'value'),
     Input('division-filter', 'value'),
     Input('division-selection', 'value')]
)
def update_belt_options(selected_event_types, selected_events, selected_division_categories, selected_division_ages):
    df_subset = apply_filters(paired_df, selected_event_types, selected_events, selected_division_categories, selected_division_ages)
    if df_subset.empty or 'Belt' not in df_subset.columns:
        return []
    belt_order = ['Yellow', 'Green', 'Blue', 'Red', 'Black']
    present = list(df_subset['Belt'].dropna().unique())
    ordered = [b for b in belt_order if b in present] + [b for b in sorted(present) if b not in belt_order]
    return [{'label': belt, 'value': belt} for belt in ordered]

@app.callback(
    Output('round-filter', 'options'),
    [Input('event-type-filter', 'value'),
     Input('event-filter', 'value'),
     Input('division-filter', 'value'),
     Input('division-selection', 'value'),
     Input('belt-filter', 'value')]
)
def update_round_options(selected_event_types, selected_events, selected_division_categories, selected_division_ages, selected_belts):
    df_subset = apply_filters(paired_df, selected_event_types, selected_events, selected_division_categories, selected_division_ages, selected_belts)
    if df_subset.empty or 'Round_Name' not in df_subset.columns:
        return []
    unique_rounds = df_subset['Round_Name'].dropna().unique()
    def round_sort_key(name):
        try:
            return -int(str(name).split()[-1])
        except Exception:
            return 0
    return [{'label': rnd, 'value': rnd} for rnd in sorted(unique_rounds, key=round_sort_key)]

@app.callback(
    [Output('kappa-display', 'children'),
     Output('kappa-interpretation', 'children'),
     Output('observed-agreement', 'children'),
     Output('expected-agreement', 'children'),
     Output('z-score', 'children'),
     Output('p-value', 'children'),
     Output('agreement-chart', 'figure'),
     Output('outcome-pie-chart', 'figure')],
    [Input('event-type-filter', 'value'),
     Input('event-filter', 'value'),
     Input('division-filter', 'value'),
     Input('division-selection', 'value'),
     Input('belt-filter', 'value'),
     Input('round-filter', 'value')]
)
def update_dashboard(selected_event_types, selected_events, selected_division_categories, selected_division_ages, selected_belts, selected_rounds):
    df_subset = apply_filters(
        paired_df,
        selected_event_types,
        selected_events,
        selected_division_categories,
        selected_division_ages,
        selected_belts,
        selected_rounds
    )

    kappa, P_bar, P_e, z_score, p_value, outcome_df, kappa_interpretation = calculate_metrics(df_subset)

    chart_data = pd.DataFrame({
        'Metric': ['Observed Agreement', 'Expected Agreement'],
        'Value': [P_bar if P_bar is not None else 0, P_e if P_e is not None else 0]
    })
    agreement_fig = px.bar(chart_data, x='Metric', y='Value',
                          title="Observed vs. Expected Agreement",
                          color='Metric', color_discrete_map={'Observed Agreement': '#1f77b4', 'Expected Agreement': '#ff7f0e'})

    if outcome_df.empty:
        outcome_fig = px.pie(names=['No Data'], values=[1], title="Match Outcomes (X-Y-Z: Agree-Disagree-Tie)")
    else:
        outcome_fig = px.pie(outcome_df, names='Outcome', values='Count',
                             title="Match Outcomes (X-Y-Z: Agree-Disagree-Tie)",
                             color_discrete_sequence=px.colors.qualitative.Set3)

    return (
        f"Fleiss' Kappa: {kappa:.3f}" if kappa is not None else "Fleiss' Kappa: N/A",
        f"Interpretation: {kappa_interpretation}",
        f"Observed Agreement: {P_bar:.3f}" if P_bar is not None else "Observed Agreement: N/A",
        f"Expected Agreement: {P_e:.3f}" if P_e is not None else "Expected Agreement: N/A",
        f"Z-Score: {z_score:.3f}" if z_score is not None and z_score != float('inf') else "Z-Score: N/A",
        f"P-Value: {p_value:.4f}" if p_value is not None else "P-Value: N/A",
        agreement_fig,
        outcome_fig
    )

if __name__ == '__main__':
    app.run(debug=True)
