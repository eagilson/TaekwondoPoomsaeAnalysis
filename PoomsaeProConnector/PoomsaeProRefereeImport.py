import json
import sqlite3
import pandas as pd

def CreateRefereeAssignment (row, refereedata, event):
    #usually only 5 judges
    position = ('R','J1','J2','J3','J4','J5','J6')
    for p in position:
        # Check if the value exists in any tuple in the Series
        if (row == p).any():
            # Get the Series name if the value is found
            referee = row[row == p].index[0]  # Returns 'b'
            refereeassignment = (event,row['Division'],row['Gender'],row['Category'],row['Round'], row['RingNbr'],'N/A',p,referee)
            refereedata.append(refereeassignment)

#connect to the database
conn = sqlite3.connect('PoomsaeProConnector/PoomsaePro.db')
curdatabase = conn.cursor()

#build the referee table
with open('PoomsaeProConnector/sql/RefereeTableCreate.sql','r') as file:
    sqlcreate = file.read()
    statements = sqlcreate.split(';')
    for sql in statements:
        curdatabase.execute(sql)
    file.close()

#import EVENTS.JSON for excel file list
with open('data/EVENTS.JSON','r') as file:
    events = json.load(file)
    file.close()

#loop over events and read in the referee position files
for event in events:
    refereedata = []
    #import as dataframe
    df = pd.read_excel('data/'+event['event']+'/'+event['refereedata'], sheet_name='Ring Assignments')
    #flatten to same form as database
    for index,row in df.iterrows():
        CreateRefereeAssignment (row, refereedata, event['event'])
    #insert into database
    sql = 'INSERT INTO RefereeAssignment VALUES ' + str(refereedata).strip('[]')                    
    curdatabase.execute(sql)

conn.commit()
curdatabase.close()