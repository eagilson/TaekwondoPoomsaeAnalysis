#Create unified database for PoomsaePro data

import pyodbc
import json
import sqlite3
from datetime import date

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
                    #adds the DatabaseID for data consistenty
                    datawid = [(DatabaseID,) + tuple(row) for row in data]
                    #remove the NONE values and Python doesn't like them
                    datawid = [tuple('None' if x is None else x for x in t) for t in datawid]
                    #update all datetime functions
                    datawid = [tuple(item.strftime('%Y-%m-%d') if isinstance(item, date) else item for item in t) for t in datawid]
                    #update data to match column count
                    curdatabase.execute(f"PRAGMA table_info("+tablename+")")
                    columns = curdatabase.fetchall()
                    column_count = len(columns)
                    datawid = [tuple(list(t) + [0] * (column_count - len(t))) for t in datawid]
                    #inserts into the master database
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
#database = sqlite3.connect(':memory:')
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
        match database['databasename']:
            case 'PP_ScoresV2c.accdb':
                extractPP_ScoresV2c(DatabaseID, database)
            case 'PP_ScoresV1c.accdb':
                print('PP_ScoresV1c.accdb code not created')
            case 'PP_ScoresV4t.accdb':
                print('PP_ScoresV4t.accdb code not created')
            case _:
                print(database['databasename']+' unknown database type.')
        

#output for testing
curdatabase.execute('SELECT * FROM Events')
for row in curdatabase.fetchall():
    print(row)

connmain.commit()
curdatabase.close()