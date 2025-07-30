#Create unified database for PoomsaePro data

import pyodbc
import json
import sqlite3
import pandas as pd
from datetime import date

def formatPP_ScoresV2c(data, DatabaseID, tablename, event, start_date):
    #format data to match current tables
    #generall formatting
    #adds the DatabaseID for data consistenty
    datawid = [(DatabaseID,) + tuple(row) for row in data]
    #remove the NONE values and Python doesn't like them
    datawid = [tuple('None' if x is None else x for x in t) for t in datawid]
    #update all datetime functions
    datawid = [tuple(item.strftime('%Y-%m-%d') if isinstance(item, date) else item for item in t) for t in datawid]

    #need code to fix the single elimination round of 4 pairing.

    #code to account for added field in V3c on SportSettings
    if database['databasename'] == 'PP_ScoresV2c.accdb' and tablename == 'SportSettings':
        df = pd.DataFrame(datawid)
        df.insert(loc=4, column='Rev',value='PP_V2c')
        datawid = [tuple(row) for row in df.to_numpy()]
    
    #code to account for DivisionNames change
    #This doesn't work for 2025 Team Trials
    if database['databasename'] == 'PP_ScoresV2c.accdb' and tablename == 'DivisionNames' and event != '2025 USATKD Team Trials':
        df = pd.DataFrame(datawid)
        df['CompMth_Black'] = df.iloc[:,6]
        df['CompOrder'] = df.iloc[:,4]
        newdf = df.iloc[:,[0,1,2,3,9,8,6,4,5,7]]
        #df[[0L,1L,2L,3L,'CompOrder','CompMeth_Black',6L,4L,5L,7L]]
        datawid = [tuple(row) for row in newdf.to_numpy()]

    #code for V3c update on 2025-07
    if start_date < '2025-07-01' and database['databasename'] == 'PP_ScoresV3c.accdb' and tablename == 'SEMatchList':
        #SEMatchList table missing NextMatch & Breaking columns
        df = pd.DataFrame(datawid)
        df.insert(loc=4, column='NextMatch',value='')
        df.insert(loc=5, column='Breaking',value=False)
        datawid = [tuple(row) for row in df.to_numpy()]

    #update data to match column count
    curdatabase.execute(f"PRAGMA table_info("+tablename+")")
    columns = curdatabase.fetchall()
    column_count = len(columns)
    datawid = [tuple(list(t) + [0] * (column_count - len(t))) for t in datawid]
    #inserts into the master database
    return datawid

def extractPP_ScoresV2c(DatabaseID, database):
    try:
        con_string = r'DRIVER={MDBTools};DBQ=' + database['path'] + ';'
        conn = pyodbc.connect(con_string)
        curevent = conn.cursor()
        cureventdata = conn.cursor()

        #Builds the Event Table
        with open('PoomsaeProConnector/sql/InsertEvents.sql','r') as file:
            sqlinsert = file.read()
            file.close()
            data = (DatabaseID,event['event'],database['day'],database['ring'],event['start-date'],event['end-date'],database['databasename'])
            curdatabase.execute(sqlinsert,data)
        
        #loop through tables in database
        for i in curevent.tables():
            tablename = i.table_name.replace(" ", "")
            if tablename in ('Round','Category','Gender'):
                tablename = tablename + 'Tbl'
            if i.table_type == 'TABLE' and tablename in curdatabasetables:
                #selects all data from the table
                sql = 'SELECT * FROM ['+ i.table_name + ']'
                cureventdata.execute(sql)
                data = cureventdata.fetchall()
                if len(data)>0:
                    datawid = formatPP_ScoresV2c(data, DatabaseID, tablename, event['event'], event['start-date'])
                    sql = 'INSERT INTO ' + tablename + ' VALUES ' + str(datawid).strip('[]')                    
                    curdatabase.execute(sql)

    except pyodbc.Error as e:
        print("Error in Connection", e)

    curevent.close()
    cureventdata.close()
    conn.close()


#Needed because the MDBTools can only do single table selects on Linux
connmain = sqlite3.connect('PoomsaeProConnector/PoomsaePro.db')
#create DB in memory for testing
#connmain = sqlite3.connect(':memory:')
curdatabase = connmain.cursor()

#build the database
with open('PoomsaeProConnector/sql/CreateSQLiteDB.sql','r') as file:
    sqlcreate = file.read()
    statements = sqlcreate.split(';')
    for sql in statements:
        curdatabase.execute(sql)
    file.close()
    
#generate list of tables for use later
with open('PoomsaeProConnector/sql/ListSQLiteTables.sql','r') as file:
    sql = file.read()
    curdatabase.execute(sql)
    curdatabasetables = curdatabase.fetchall()
    curdatabasetables = [item[0] for item in curdatabasetables]
    file.close()

#read EVENTS.JSON for list of event databases
with open('data/EVENTS.JSON','r') as file:
    events = json.load(file)
    file.close()

#iterate over databases to pull the data
#Count the distinct databases
DatabaseID = 0

for event in events:
    for database in event['databases']:
        #increment the Database ID for unique keying
        DatabaseID+=1
        #insert logic for different Poomsae Pro database types
        #code below is for PP_ScoresV2c.accdb

        #Connect to MS Access Database
        print(event['event'])
        match database['databasename']:
            case 'PP_ScoresV1b.accdb': #Breaking
                print(database['databasename']+' code not created')
            case 'PP_ScoresV2F.accdb': #Freestyle
                print(database['databasename']+' code not created')
            case 'PP_ScoresV3a.accdb': #Recognized
                print(database['databasename']+' code not created')
            case 'PP_ScoresV4a.accdb': #Recognized
                print(database['databasename']+' code not created')
            case 'PP_ScoresV3t.accdb': #Team Trials
                print(database['databasename']+' code not created')
            case 'PP_ScoresV4t.accdb': #Team Trials
                print(database['databasename']+' code not created')
            case 'PP_ScoresV1c.accdb': #Combo
                print(database['databasename']+' code not created')
            case 'PP_ScoresV2c.accdb': #Combo
                extractPP_ScoresV2c(DatabaseID, database)
            case 'PP_ScoresV3c.accdb': #Combo for Simultaneous
                #V2c and V3c only differ by the SEMatchList table
                #DivisionNames table has a different column layout
                extractPP_ScoresV2c(DatabaseID, database)
            case _:
                print(database['databasename']+' unknown database type.')
        

#output for testing
curdatabase.execute('SELECT * FROM Events')
for row in curdatabase.fetchall():
    print(row)

connmain.commit()
curdatabase.close()