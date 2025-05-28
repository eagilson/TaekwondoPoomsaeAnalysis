import json
import sqlite3
import pandas as pd
from pathlib import Path

def worksheet_exists(file_path, sheet_name):
    """Function to determine if a worksheet exists"""
    # Check if file exists and is an Excel file
    file_path = Path(file_path).resolve()  # Normalize path
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        return False
    
    if file_path.suffix.lower() not in ('.xlsx', '.xlsm'):
        print(f"Error: File '{file_path}' is not a supported Excel file (.xlsx or .xlsm).")
        return False
    
    try:
        # Load the Excel file with pandas
        excel_file = pd.ExcelFile(file_path)
        # Check if the sheet exists
        return sheet_name in excel_file.sheet_names
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

#connect to the database
conn = sqlite3.connect('PoomsaeProConnector/PoomsaePro.db')
curdatabase = conn.cursor()

#import EVENTS.JSON for excel file list
with open('data/EVENTS.JSON','r') as file:
    events = json.load(file)
    file.close()

#prepare SQL
with open('PoomsaeProConnector/sql/CreateExcelData.sql','r') as file:
    sql = file.read()
    file.close()

#standard sheet name
sheetname = 'Ring Assignments'

#loop over events
for event in events:
    #check if excel file exists with sheet
    excelfilepath = event['path']+'/'+event['refereedata']
    
    if not worksheet_exists(excelfilepath, sheetname) and event['database-type'] == 'PoomsaePro':
        #extract data for sheet creation
        data = {'eventname':event['event']}
        curdatabase.execute(sql, data)
        divisionlist = curdatabase.fetchall()
        columns = ['Division','Gender','Category','Round','RingNbr']
        df = pd.DataFrame(divisionlist, columns=columns)

        #update json with new file name
        event['refereedata'] = event['event']+'.xlsx'

        #populate excel sheet
        excelfilepath = event['path']+'/'+event['refereedata']
        with pd.ExcelWriter(excelfilepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheetname, index=False)

#update EVENTS file with new data
with open('data/EVENTS.JSON', 'w') as file:
    json.dump(events, file, indent=4)     
    file.close()
    
curdatabase.close()