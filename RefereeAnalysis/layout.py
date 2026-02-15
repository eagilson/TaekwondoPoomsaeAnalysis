# layout.py
from dash import dcc, html, dash_table


def layout(app, df, raw_data_columns):
    """Defines the layout of the Dash App."""
    app.layout = html.Div([
        html.H1("Referee Scoring Performance Dashboard"),

        # ────── FILTERS ──────
        html.Div([
            html.Div([
                html.Label("Event:"),
                dcc.Dropdown(
                    id='event-filter',
                    options=[{'label': e, 'value': e} for e in sorted(df['EventName'].unique())],
                    value=None,
                    multi=True,
                    placeholder="Select Event(s)"
                ),
            ], style={'marginBottom': 20, 'width': '48%', 'marginRight': '2%'}),
            html.Div([
                html.Label("Referee Name:"),
                dcc.Dropdown(
                    id='referee-filter',
                    options=[{'label': n, 'value': n} for n in sorted(df['RefereeName'].unique())],
                    value=None,
                    multi=True,
                    placeholder="Select Referee(s)"
                ),
            ], style={'marginBottom': 20, 'width': '48%'}),
            html.Div([
                html.Label("Event Category:"),
                dcc.Dropdown(
                    id='category-filter',
                    options=[{'label': c, 'value': c} for c in sorted(df['Event_Category'].unique())],
                    value=None,
                    multi=False,
                    placeholder="Select Event Category"
                ),
            ], style={'marginBottom': 20, 'width': '48%', 'marginRight': '2%'}),
            html.Div([
                html.Label("Belt:"),
                dcc.Dropdown(
                    id='belt-filter',
                    options=[{'label': b, 'value': b} for b in sorted(df['Belt'].unique())],
                    value=None,
                    multi=True,
                    placeholder="Select Belt(s)"
                ),
            ], style={'marginBottom': 20, 'width': '48%'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap'}),

        # ────── TABS ──────
        dcc.Tabs([
            # ── Summary Statistics ──
            dcc.Tab(label='Summary Statistics', children=[
                dcc.Loading(
                    id="loading-stats",
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
                            data=[],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '5px',
                                        'minWidth': '100px', 'maxWidth': '200px'},
                            style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'},
                            page_size=10,
                            sort_action='native',
                            filter_action='native',
                        )
                    ]
                )
            ]),

            # ── Score Detail ──
            dcc.Tab(label='Score Detail', children=[
                dcc.Loading(
                    id="loading-raw",
                    type="circle",
                    children=[
                        dash_table.DataTable(
                            id='raw-data-table',
                            columns=raw_data_columns,
                            data=[],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'padding': '5px',
                                        'minWidth': '100px', 'maxWidth': '200px'},
                            style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'},
                            page_size=10,
                            sort_action='native',
                            filter_action='native',
                        )
                    ]
                )
            ]),

            # ── Score Difference Box Plots + Bar Charts ──
            dcc.Tab(label='Score Difference Histogram', children=[
                html.Div([
                    html.H3("Distribution of Referee Score Differences from the Final Score", 
                            style={'textAlign': 'center', 'margin': '20px 0 10px'}),
                    dcc.Loading(
                        id="loading-histograms",
                        type="circle",
                        children=[
                            # ── ROW 1 : Box Plots ──
                            # html.Div([
                            #     dcc.Graph(
                            #         id='acc-diff-boxplot',
                            #         style={'width': '50%', 'padding': '10px'}
                            #     ),
                            #     dcc.Graph(
                            #         id='pre-diff-boxplot',
                            #         style={'width': '50%', 'padding': '10px'}
                            #     )
                            # ], style={'display': 'flex', 'flexWrap': 'nowrap',
                            #           'justifyContent': 'space-between', 'width': '100%'}),

                            # ── ROW 2 : Bar Charts ──
                            html.Div([
                                dcc.Graph(
                                    id='acc-diff-bar',
                                    style={'width': '50%', 'padding': '10px'}
                                ),
                                dcc.Graph(
                                    id='pre-diff-bar',
                                    style={'width': '50%', 'padding': '10px'}
                                )
                            ], style={'display': 'flex', 'flexWrap': 'nowrap',
                                      'justifyContent': 'space-between', 'width': '100%'})
                        ]
                    )
                ])
            ]),

            # ── Single Elimination Referee Gaps ──
            dcc.Tab(label='Single Elimination Referee Gaps', children=[
                html.Div([
                    html.H3("Referee Score Gaps Between the Winner & Loser in Single Elimination", 
                            style={'textAlign': 'center', 'margin': '20px 0 10px'}),
                    dcc.Loading(
                        id="loading-se-gaps",
                        type="circle",
                        children=[
                            # ── Gap Distribution per Referee ──
                            html.Div([
                                dcc.Graph(
                                    id='se-acc-gap-bar',
                                    style={'width': '50%', 'padding': '10px'}
                                ),
                                dcc.Graph(
                                    id='se-pre-gap-bar',
                                    style={'width': '50%', 'padding': '10px'}
                                ),
                            ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%'})
                        ]
                    )
                ])
            ])
        ])
    ])