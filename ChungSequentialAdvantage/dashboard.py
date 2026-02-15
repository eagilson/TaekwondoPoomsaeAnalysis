import dash
from ChungSequentialAdvantage.database import build_database
from ChungSequentialAdvantage.callbacks import register_callbacks
from ChungSequentialAdvantage.layout import layout

# Load data
db_path = 'PoomsaeProConnector/PoomsaePro.db'
sql_file_path = 'sql/RoundWinner.sql'
df = build_database(db_path, sql_file_path)

# Initialize Dash app
app = dash.Dash(__name__)

register_callbacks(app, df)

layout(app, df)

if __name__ == '__main__':
    app.run(debug=True)