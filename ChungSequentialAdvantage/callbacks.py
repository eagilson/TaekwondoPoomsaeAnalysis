# callbacks.py
import pandas as pd
from dash.dependencies import Input, Output
from dash import html
import plotly.express as px
from ChungSequentialAdvantage.data_processing import binomial_test, calculate_win_rates_by_division, calculate_win_rates_by_event


def register_callbacks(app, df: pd.DataFrame):
    """Register Dash callbacks for the app."""

    # Callback to update graph and stats
    @app.callback(
        [Output('win-rate-bar', 'figure'), Output('stats-output', 'children')],
        [
            Input('event-filter', 'value'),
            Input('division-category-filter', 'value'),
            Input('simultaneous-filter', 'value'),
            Input('draw-type-filter', 'value')
            ]
    )
    def update_graph(event, division, simultaneous, draw_type):
        # Filter for Sequential matches and EventName
        filtered_df = df
        if event:
            filtered_df = filtered_df[filtered_df['EventName'].isin(event)]
        if division:
            filtered_df = filtered_df[filtered_df['division_category'].isin(division)]
        if simultaneous:
            filtered_df = filtered_df[filtered_df['Simultaneous'] == simultaneous]
        if draw_type:
            filtered_df = filtered_df[filtered_df['draw_type'] == draw_type]
        
        # Compute win rates and test results
        win_rate_df = calculate_win_rates_by_event(filtered_df)
        test_results = []
        for _, row in win_rate_df.iterrows():
            _, p_value = binomial_test(row['Hong Wins'], row['Total Matches'])
            test_results.append({
                'EventName': row['EventName'],
                'P-value': p_value,
                'Conclusion': 'Significant difference' if p_value < 0.05 else 'No significant difference'
            })
        test_results_df = pd.DataFrame(test_results)
        
        # Merge results for display
        display_df = win_rate_df.merge(test_results_df, on='EventName')
        
        # Create bar plot
        fig = px.bar(win_rate_df, x='EventName', y='Win Rate', 
                    color='EventName')
        fig.update_layout(yaxis_title="Hong Win Rate", yaxis_tickformat=".2%", 
                        shapes=[dict(type='line', x0=-0.5, x1=len(win_rate_df)-0.5, y0=0.5, y1=0.5, 
                                    line=dict(color='red', dash='dash'))],
                        showlegend=False)
        
        # Statistical test results
        stats_text = [
            html.H3("Statistical Test Results:"),
            html.Ul([
                html.Li([
                    f"{row['EventName']}: ",
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







        """ 
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
                    title=f"Hong's Win Rate in Sequential Matches by Division Type ({', '.join(event) if event else 'All Events'})",
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
        
        return fig, stats_text """

