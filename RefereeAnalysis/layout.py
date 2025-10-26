from dash import dcc, html, dash_table

def layout(app, df, raw_data_columns):
    """Definels the layout of the Dash App."""
    # Layout
    app.layout = html.Div([
        html.H1("Referee Scoring Performance Dashboard"),
        html.Div([
            html.Div([
                html.Label("Event:"),
                dcc.Dropdown(
                    id='event-filter',
                    options=[{'label': event, 'value': event} for event in sorted(df['EventName'].unique())],
                    value=None,
                    multi=True,
                    placeholder="Select Event(s)"
                ),
            ], style={'marginBottom': 20, 'width': '48%', 'marginRight': '2%'}),
            html.Div([
                html.Label("Referee Name:"),
                dcc.Dropdown(
                    id='referee-filter',
                    options=[{'label': name, 'value': name} for name in sorted(df['RefereeName'].unique())],
                    value=None,
                    multi=True,
                    placeholder="Select Referee(s)"
                ),
            ], style={'marginBottom': 20, 'width': '48%'}),
            html.Div([
                html.Label("Event Category:"),
                dcc.Dropdown(
                    id='category-filter',
                    options=[{'label': cat, 'value': cat} for cat in sorted(df['Event_Category'].unique())],
                    value=None,
                    multi=False,
                    placeholder="Select Event Category"
                ),
            ], style={'marginBottom': 20, 'width': '48%', 'marginRight': '2%'}),
            html.Div([
                html.Label("Belt:"),
                dcc.Dropdown(
                    id='belt-filter',
                    options=[{'label': belt, 'value': belt} for belt in sorted(df['Belt'].unique())],
                    value=None,
                    multi=True,
                    placeholder="Select Belt(s)"
                ),
            ], style={'marginBottom': 20, 'width': '48%'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap'}),
        dcc.Tabs([
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
                            style_cell={'textAlign': 'left', 'padding': '5px', 'minWidth': '100px', 'maxWidth': '200px'},
                            style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'},
                            page_size=10,
                            sort_action='native',
                            filter_action='native',
                        )
                    ]
                )
            ]),
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
                            style_cell={'textAlign': 'left', 'padding': '5px', 'minWidth': '100px', 'maxWidth': '200px'},
                            style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'},
                            page_size=10,
                            sort_action='native',
                            filter_action='native',
                        )
                    ]
                )
            ]),
            dcc.Tab(label='Score Difference Box Plots', children=[
                dcc.Loading(
                    id="loading-histograms",
                    type="circle",
                    children=[
                        html.Div([
                            dcc.Graph(id='acc-diff-boxplot', style={'width': '50%', 'padding': '10px'}),
                            dcc.Graph(id='pre-diff-boxplot', style={'width': '50%', 'padding': '10px'})
                        ], style={'display': 'flex', 'flexWrap': 'nowrap', 'justifyContent': 'space-between', 'width': '100%'})
                    ]
                )
            ])
        ])
    ])