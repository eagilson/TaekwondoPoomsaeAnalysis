# layout.py
from dash import dcc, html, dash_table


def layout(app, df):
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