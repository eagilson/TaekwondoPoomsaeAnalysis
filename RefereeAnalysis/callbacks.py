# callbacks.py
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from RefereeAnalysis.data_processing import compute_stats


def register_callbacks(app, df: pd.DataFrame, raw_data_columns):
    """Register Dash callbacks for the app."""

    # ── Update referee dropdown based on selected events ──
    @app.callback(
        Output('referee-filter', 'options'),
        Input('event-filter', 'value')
    )
    def update_referee_options(selected_events):
        if not selected_events:
            return [{'label': name, 'value': name} for name in sorted(df['RefereeName'].unique())]
        filtered_df = df[df['EventName'].isin(selected_events)]
        return [{'label': name, 'value': name} for name in sorted(filtered_df['RefereeName'].unique())]

    # ── Update tables + box plots + bar charts ──
    @app.callback(
        [
            Output('stats-table', 'data'),
            Output('raw-data-table', 'data'),
            Output('acc-diff-boxplot', 'figure'),
            Output('pre-diff-boxplot', 'figure'),
            Output('acc-diff-bar', 'figure'),
            Output('pre-diff-bar', 'figure')
        ],
        [
            Input('referee-filter', 'value'),
            Input('event-filter', 'value'),
            Input('category-filter', 'value'),
            Input('belt-filter', 'value')
        ]
    )
    def update_tables_and_plots(referee, event, category, belt):
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

        if filtered_df.empty:
            empty_fig = {'data': [], 'layout': {}}
            return [], [], empty_fig, empty_fig, empty_fig, empty_fig

        # ── Compute stats & collect differences ──
        all_acc_diffs = []
        all_pre_diffs = []
        stats_df = filtered_df.groupby(['RefereeName', 'EventName', 'Event_Category']).apply(
            lambda g: compute_stats(g)[0], include_groups=False
        ).reset_index()

        for _, group in filtered_df.groupby(['RefereeName', 'EventName', 'Event_Category']):
            _, acc_diffs, pre_diffs = compute_stats(group)
            if not acc_diffs.empty:
                all_acc_diffs.extend(acc_diffs)
            if not pre_diffs.empty:
                all_pre_diffs.extend(pre_diffs)

        all_acc_diffs = pd.Series(all_acc_diffs)
        all_pre_diffs = pd.Series(all_pre_diffs)

        # Round stats
        numeric_cols = ['Correlation', 'Presentation_Diff_SD', 'Accuracy_Diff_SD',
                        'Presentation_Diff_Mean', 'Accuracy_Diff_Mean']
        stats_df[numeric_cols] = stats_df[numeric_cols].round(3).fillna('-')

        # Raw data
        raw_data_cols = [col['id'] for col in raw_data_columns]
        raw_data = filtered_df[raw_data_cols].copy()

        # ── Bar Charts ──
        def make_bar_chart(data_series, title, color):
            if data_series.empty:
                return {'data': [], 'layout': {}}

            # auto bin resolution
            hist, bin_edges = np.histogram(data_series.dropna(), bins='auto', density=True)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            return {
                'data': [{
                    'type': 'bar',
                    'x': bin_centers,
                    'y': hist,
                    'marker': {'color': color},
                    'hovertemplate': 'Diff: %{x:.3f}<br>Count: %{y}<extra></extra>'
                }],
                'layout': {
                    'title': title,
                    'xaxis': {'title': 'Score Difference'},
                    'yaxis': {'title': 'Count'},
                    'bargap': 0.05
                }
            }

        # ── Box Plots ──
        def make_box_chart(data_series, title, color):
            if data_series.empty:
                return {'data': [], 'layout': {}}
            
            return {
                'data': [{
                    'type': 'box',
                    'y': all_pre_diffs.dropna().tolist(),
                    'name': 'Score Difference',
                    'marker': {'color': color},
                    'notched': True,
                    'boxpoints': 'outliers',
                    'jitter': 0.3,
                    'pointpos': 0
                }],
                'layout': {
                    'title': title,
                    'yaxis': {'title': 'Score Difference'},
                    'xaxis': {'showticklabels': False},
                    'showlegend': False
                    }
                }

        acc_box = make_box_chart(all_acc_diffs, 'Accuracy Difference Distribution', '#1f77b4')
        pre_box = make_box_chart(all_pre_diffs, 'Box Plot of Presentation Differences', '#ff7f0e')

        acc_bar = make_bar_chart(all_acc_diffs, 'Accuracy Difference', '#1f77b4')
        pre_bar = make_bar_chart(all_pre_diffs, 'Presentation Difference', '#ff7f0e')

        return (
            stats_df.to_dict('records'),
            raw_data.to_dict('records'),
            acc_box,
            pre_box,
            acc_bar,
            pre_bar
        )