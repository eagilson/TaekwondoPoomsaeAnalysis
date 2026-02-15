# layout.py
from dash import dcc, html


def layout(app, df):
    app.layout = html.Div([
        html.H1("Hong's Win Rate Analysis"),
        
        # ────── FILTERS ──────
        html.Div([
            html.Div([
                html.Label("Event:"),
                dcc.Dropdown(  
                    id='event-filter',
                    options=[{'label': event, 'value': event} for event in sorted(df['EventName'].unique())],
                    value=None,
                    placeholder="Select Events (All Events if None Selected)",
                    multi=True
                )
            ], style={'marginBottom': 20, 'width': '48%', 'marginRight': '2%'}), 
            html.Div([
                html.Label("Division Category:"),
                dcc.Dropdown(  
                    id='division-category-filter',
                    options=[{'label': division_category, 'value': division_category} for division_category in sorted(df['division_category'].unique())],
                    value=None,
                    placeholder="Select Division Category (All Categories if None Selected)",
                    multi=True
                )
            ], style={'marginBottom': 20, 'width': '48%', 'marginRight': '2%'}),
            html.Div([
                html.Label("Competition Order:"),
                dcc.Dropdown(  
                    id='simultaneous-filter',
                    options=[{'label': Simultaneous, 'value': Simultaneous} for Simultaneous in sorted(df['Simultaneous'].unique())],
                    value=None,
                    placeholder="Sequential or Simultaneous",
                    multi=False
                )
            ], style={'marginBottom': 20, 'width': '48%', 'marginRight': '2%'}),
            html.Div([
                html.Label("Draw Type:"),
                dcc.Dropdown(  
                    id='draw-type-filter',
                    options=[{'label': draw_type, 'value': draw_type} for draw_type in sorted(df['draw_type'].unique())],
                    value=None,
                    placeholder="Designated or Random",
                    multi=False
                )
            ], style={'marginBottom': 20, 'width': '48%', 'marginRight': '2%'}), 
            
        ], style={'display': 'flex', 'flexWrap': 'wrap'}),
        dcc.Graph(id='win-rate-bar'),
        html.Div(id='stats-output')
    ])