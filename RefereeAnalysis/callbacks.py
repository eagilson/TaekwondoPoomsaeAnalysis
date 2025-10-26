import pandas as pd
from dash.dependencies import Input, Output
from RefereeAnalysis.data_processing import compute_stats

def register_callbacks(app, df:pd.DataFrame, raw_data_columns):
    """Register Dash callbacks for the app."""
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

    # Callback to update tables and box plots based on filters
    @app.callback(
        [
            Output('stats-table', 'data'),
            Output('raw-data-table', 'data'),
            Output('acc-diff-boxplot', 'figure'),
            Output('pre-diff-boxplot', 'figure')
        ],
        [
            Input('referee-filter', 'value'),
            Input('event-filter', 'value'),
            Input('category-filter', 'value'),
            Input('belt-filter', 'value')
        ]
    )
    def update_tables_and_boxplots(referee, event, category, belt):
        # Start with full df
        filtered_df = df.copy()
        
        # Apply filters
        if referee:
            filtered_df = filtered_df[filtered_df['RefereeName'].isin(referee)]
        if event:
            filtered_df = filtered_df[filtered_df['EventName'].isin(event)]
        if category:
            filtered_df = filtered_df[filtered_df['Event_Category'] == category]
        if belt:
            filtered_df = filtered_df[filtered_df['Belt'].isin(belt)]
        
        # Compute stats_df based on filtered data
        if filtered_df.empty:
            return [], [], {'data': [], 'layout': {}}, {'data': [], 'layout': {}}
        
        # Collect all acc_diffs and pre_diffs across groups
        all_acc_diffs = []
        all_pre_diffs = []
        stats_df = filtered_df.groupby(['RefereeName', 'EventName', 'Event_Category']).apply(
            lambda g: compute_stats(g)[0], include_groups=False
        ).reset_index()
        
        # Collect differences for box plots
        for _, group in filtered_df.groupby(['RefereeName', 'EventName', 'Event_Category']):
            _, acc_diffs, pre_diffs = compute_stats(group)
            if not acc_diffs.empty:
                all_acc_diffs.extend(acc_diffs)
            if not pre_diffs.empty:
                all_pre_diffs.extend(pre_diffs)
        
        all_acc_diffs = pd.Series(all_acc_diffs)
        all_pre_diffs = pd.Series(all_pre_diffs)
        
        # Round numeric columns for display to 3 decimal places
        numeric_cols = ['Correlation', 'Presentation_Diff_SD', 'Accuracy_Diff_SD', 'Presentation_Diff_Mean', 'Accuracy_Diff_Mean']
        stats_df[numeric_cols] = stats_df[numeric_cols].round(3)
        stats_df[numeric_cols] = stats_df[numeric_cols].fillna('-')
        
        # Select columns for raw data table
        raw_data_cols = [col['id'] for col in raw_data_columns]
        raw_data = filtered_df[raw_data_cols].copy()
        
        # Create Plotly box plots
        acc_diff_boxplot = {
            'data': [{
                'type': 'box',
                'y': all_acc_diffs.dropna().tolist(),
                'name': 'Accuracy Difference',
                'marker': {'color': '#1f77b4'},
                'notched':True,
                'boxpoints': 'outliers',
                'jitter': 0.3,
                'pointpos': 0
            }],
            'layout': {
                'title': {'text': 'Box Plot of Accuracy Differences'},
                'yaxis': {'title': 'Accuracy Difference'},
                'xaxis': {'showticklabels': False},
                'showlegend': False
            }
        }
        
        pre_diff_boxplot = {
            'data': [{
                'type': 'box',
                'y': all_pre_diffs.dropna().tolist(),
                'name': 'Presentation Difference',
                'marker': {'color': '#ff7f0e'},
                'notched':True,
                'boxpoints': 'outliers',
                'jitter': 0.3,
                'pointpos': 0
            }],
            'layout': {
                'title': {'text': 'Box Plot of Presentation Differences'},
                'yaxis': {'title': 'Presentation Difference'},
                'xaxis': {'showticklabels': False},
                'showlegend': False
            }
        }
        
        return (
            stats_df.to_dict('records'),
            raw_data.to_dict('records'),
            acc_diff_boxplot,
            pre_diff_boxplot
        )