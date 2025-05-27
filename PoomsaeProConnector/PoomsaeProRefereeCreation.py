import json
import sqlite3
import pandas as pd

#connect to the database
conn = sqlite3.connect('PoomsaeProConnector/PoomsaePro.db')
curdatabase = conn.cursor()
sql = 'SELECT * FROM Events'
curdatabase.execute(sql)
for row in curdatabase.fetchall():
    print(row)

#import EVENTS.JSON for excel file list
with open('data/EVENTS.JSON','r') as file:
    events = json.load(file)
    file.close()

#prepare SQL
with open('PoomsaeProConnector/sql/CreateExcelData.sql','r') as file:
    sql = file.read()
    file.close()

#loop over events
for event in events:
    #check if excel file exists with sheet
    data = {'eventname':event['event']}
    #print(sql)
    curdatabase.execute(sql, data)
    divisionlist = curdatabase.fetchall()
    #populate excel sheet
    

curdatabase.close()