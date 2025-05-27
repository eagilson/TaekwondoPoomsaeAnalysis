import json
import sqlite3
import pandas as pd

#connect to the database
database = sqlite3.connect('PoomsaeProConnector/PoomsaePro.db')
curdatabase = database.cursor()

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
    print(event['event'],event['refereedata'])
    #import as dataframe
    #flatten
    #add event name
    #insert into database

curdatabase.close()