import pandas as pd
from scipy.stats import binomtest
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from utils import load_data, categorize_division

db_path = 'PoomsaeProConnector/PoomsaePro.db'
sql_file_path = 'sql/RoundWinner.sql'

# Load initial data for dropdown options
df = load_data(db_path, sql_file_path)

# Data cleaning
df = df.dropna(subset=['Winner', 'Simultaneous', 'Division', 'EventName'])
df['Simultaneous'] = df['Simultaneous'].astype(int)  # Ensure 0/1

# Categorize divisions
df['division_category'] = df['Division'].apply(categorize_division)
df['division_group'] = df['division_category'].apply(lambda x: 'Pair & Team' if x in ['Pair', 'Team'] else 'Individual')

# Calculate win rates by division group
def calculate_win_rates_by_division(seq_df):
    grouped = seq_df.groupby('division_group')
    results = []
    
    for division, group in grouped:
        hong_wins = len(group[group['Winner'] == 'Hong'])
        total_matches = len(group)
        win_rate = hong_wins / total_matches if total_matches > 0 else 0
        results.append({
            'Division Group': division,
            'Hong Wins': hong_wins,
            'Total Matches': total_matches,
            'Win Rate': win_rate
        })
    
    return pd.DataFrame(results)

# Two-sided binomial test
def binomial_test(wins, total):
    if total == 0:
        return 0, 1.0  # No matches, no significance
    result = binomtest(wins, total, p=0.5, alternative='two-sided')
    return 0, result.pvalue  # Return 0 for statistic (not used)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with multi-select EventName dropdown
app.layout = html.Div([
    html.H1("Hong's Win Rate Analysis in Sequential Taekwondo Poomsae Matches"),
    dcc.Dropdown(
        id='event-dropdown',
        options=[{'label': event, 'value': event} for event in sorted(df['EventName'].unique())],
        value=None,
        placeholder="Select Events (All Events if None Selected)",
        multi=True,
        style={
            'width': '60%',
            'margin': '20px auto',
            'fontSize': 16,
            'padding': '5px',
            'borderRadius': '5px',
            'border': '1px solid #ccc',
            'backgroundColor': '#f9f9f9'
        }
    ),
    dcc.Graph(id='win-rate-bar'),
    html.Div(id='stats-output')
])

# Callback to update graph and stats
@app.callback(
    [Output('win-rate-bar', 'figure'), Output('stats-output', 'children')],
    [Input('event-dropdown', 'value')]
)
def update_graph(event_filter):
    # Filter for Sequential matches and EventName
    filtered_df = df[df['Simultaneous'] == 0]
    if event_filter:
        filtered_df = filtered_df[filtered_df['EventName'].isin(event_filter)]
    
    # Compute win rates and test results
    win_rate_df = calculate_win_rates_by_division(filtered_df)
    test_results = []
    for _, row in win_rate_df.iterrows():
        _, p_value = binomial_test(row['Hong Wins'], row['Total Matches'])
        test_results.append({
            'Division Group': row['Division Group'],
            'P-value': p_value,
            'Conclusion': 'Significant difference' if p_value < 0.05 else 'No significant difference'
        })
    test_results_df = pd.DataFrame(test_results)
    
    # Merge results for display
    display_df = win_rate_df.merge(test_results_df, on='Division Group')
    
    # Create bar plot
    fig = px.bar(win_rate_df, x='Division Group', y='Win Rate', 
                 title=f"Hong's Win Rate in Sequential Matches by Division Type ({', '.join(event_filter) if event_filter else 'All Events'})",
                 color='Division Group', 
                 color_discrete_map={'Pair & Team': '#1f77b4', 'Individual': '#ff7f0e'})
    fig.update_layout(yaxis_title="Win Rate", yaxis_tickformat=".2%", 
                      shapes=[dict(type='line', x0=-0.5, x1=1.5, y0=0.5, y1=0.5, 
                                   line=dict(color='red', dash='dash'))])
    
    # Statistical test results
    stats_text = [
        html.H3("Statistical Test Results:"),
        html.Ul([
            html.Li([
                f"{row['Division Group']}: ",
                html.Br(),
                f"  - Wins: {int(row['Hong Wins'])}/{int(row['Total Matches'])} ({row['Win Rate']:.2%})",
                html.Br(),
                f"  - P-value: {row['P-value']:.4f}",
                html.Br(),
                f"  - Conclusion: {row['Conclusion']} (p < 0.05)"
            ]) for _, row in display_df.iterrows()
        ])
    ]
    
    return fig, stats_text

# Run Dash app
if __name__ == '__main__':
    app.run(debug=True)