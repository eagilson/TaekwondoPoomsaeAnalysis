import dash
from RefereeAnalysis.database import build_database
from RefereeAnalysis.callbacks import register_callbacks
from RefereeAnalysis.layout import layout

# Load data
db_path = 'PoomsaeProConnector/PoomsaePro.db'
sql_file_path = 'sql/RefereeFullScore.sql'
df = build_database(db_path, sql_file_path)

# Initialize Dash app
app = dash.Dash(__name__)

# Define columns for raw data table
raw_data_columns = [
    {'name': 'Event Name', 'id': 'EventName'},
    {'name': 'Referee Name', 'id': 'RefereeName'},
    {'name': 'Division', 'id': 'Division'},
    {'name': 'Gender', 'id': 'Gender'},
    {'name': 'Category', 'id': 'Category'},
    {'name': 'Round', 'id': 'Round'},
    {'name': 'Match Number', 'id': 'MatchNo'},
    {'name': 'Performance ID', 'id': 'Performance_ID'},
    {'name': 'Accuracy A', 'id': 'Accuracy_A'},
    {'name': 'Presentation A', 'id': 'Presentation_A'},
    {'name': 'Accuracy B', 'id': 'Accuracy_B'},
    {'name': 'Presentation B', 'id': 'Presentation_B'},
    {'name': 'Accuracy T', 'id': 'Accuracy_T'},
    {'name': 'Presentation T', 'id': 'Presentation_T'},
    {'name': 'Referee Placement', 'id': 'Referee_Placement'},
    {'name': 'Official Placement', 'id': 'Placement'},
]

register_callbacks(app, df, raw_data_columns)

layout(app, df, raw_data_columns)

if __name__ == '__main__':
    app.run(debug=True)