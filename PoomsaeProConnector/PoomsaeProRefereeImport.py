import json
import sqlite3
import pandas as pd
from pathlib import Path

from utils import worksheet_exists

def CreateRefereeAssignment (row, refereedata, event):
    #usually only 5 judges
    position = ('R','J1','J2','J3','J4','J5','J6')
    for p in position:
        # Check if the value exists in any tuple in the Series
        if (row == p).any():
            #Get the column name to find the referee name
            referee = row[row == p].index[0]  
            #statement for V3c databases with Match Numbers
            if 'MatchNo' in row.index:
                refereeassignment = (event,row['Division'],row['Gender'],row['Category'],row['Round'],row['RingNbr'],row['MatchNo'],p,referee)
            else:
                refereeassignment = (event,row['Division'],row['Gender'],row['Category'],row['Round'],row['RingNbr'],'',p,referee)
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
    #note this adds the referee data independent of if the event is in the database
    refereedata = []
    #import as dataframe
    excelfilepath = event['path']+'/'+event['refereedata']
    if worksheet_exists(excelfilepath, 'Ring Assignments'):
        df = pd.read_excel(event['path']+'/'+event['refereedata'], sheet_name='Ring Assignments', dtype={'MatchNo': str}, na_filter=False)
        #flatten to same form as database
        for index,row in df.iterrows():
            CreateRefereeAssignment (row, refereedata, event['event'])
        #insert into database
        if not refereedata:
            print('No data for '+event['event'])
        else:
            sql = 'INSERT INTO RefereeAssignment VALUES ' + str(refereedata).strip('[]')     
            curdatabase.execute(sql)

conn.commit()
curdatabase.close()