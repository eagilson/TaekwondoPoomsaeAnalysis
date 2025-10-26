# callbacks.py
import pandas as pd
from dash.dependencies import Input, Output
from RefereeAnalysis.data_processing import compute_stats, singleeliminationgaps
from RefereeAnalysis.charts import make_bar_chart, make_box_chart


def register_callbacks(app, df: pd.DataFrame, raw_data_columns):
    """Register Dash callbacks for the app."""

    @app.callback(
        Output('referee-filter', 'options'),
        Input('event-filter', 'value')
    )
    def update_referee_options(selected_events):
        if not selected_events:
            return [{'label': name, 'value': name} for name in sorted(df['RefereeName'].unique())]
        filtered_df = df[df['EventName'].isin(selected_events)]
        return [{'label': name, 'value': name} for name in sorted(filtered_df['RefereeName'].unique())]

    @app.callback(
        [
            Output('stats-table', 'data'),
            Output('raw-data-table', 'data'),
            Output('acc-diff-boxplot', 'figure'),
            Output('pre-diff-boxplot', 'figure'),
            Output('acc-diff-bar', 'figure'),
            Output('pre-diff-bar', 'figure'),
            Output('se-acc-gap-bar', 'figure'),
            Output('se-pre-gap-bar', 'figure')
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
            return [], [], empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

        # ── All Rounds: Score Differences ──
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

        # Box & Bar (All Rounds)
        acc_box = make_box_chart(all_acc_diffs, 'Accuracy Difference Distribution', '#1f77b4')
        pre_box = make_box_chart(all_pre_diffs, 'Presentation Difference Distribution', '#ff7f0e')
        acc_bar = make_bar_chart(all_acc_diffs, 'Accuracy Difference Distribution', '#1f77b4', 0.03)
        pre_bar = make_bar_chart(all_pre_diffs, 'Presentation Difference Distribution', '#ff7f0e', 0.03)

        # Raw data
        raw_data_cols = [col['id'] for col in raw_data_columns]
        raw_data = filtered_df[raw_data_cols].copy()

        # ── Single Elimination: Aggregate Gaps (A, B, T) ──
        gap_df = singleeliminationgaps(filtered_df)

        # Safe extraction: only use columns that exist
        acc_gap_cols = [col for col in ['Accuracy_A_Gap', 'Accuracy_B_Gap', 'Accuracy_T_Gap'] if col in gap_df.columns]
        pre_gap_cols = [col for col in ['Presentation_A_Gap', 'Presentation_B_Gap', 'Presentation_T_Gap'] if col in gap_df.columns]

        # Default to empty series if no columns
        acc_gaps_series = pd.concat([gap_df[col] for col in acc_gap_cols], ignore_index=True) if acc_gap_cols else pd.Series()
        pre_gaps_series = pd.concat([gap_df[col] for col in pre_gap_cols], ignore_index=True) if pre_gap_cols else pd.Series()

        se_acc_gap_bar = make_bar_chart(
            acc_gaps_series,
            'Single Elimination: Accuracy Gap Distribution',
            '#1f77b4'
        )

        se_pre_gap_bar = make_bar_chart(
            pre_gaps_series,
            'Single Elimination: Presentation Gap Distribution',
            '#ff7f0e'
        )

        return (
            stats_df.to_dict('records'),
            raw_data.to_dict('records'),
            acc_box,
            pre_box,
            acc_bar,
            pre_bar,
            se_acc_gap_bar,
            se_pre_gap_bar
        )