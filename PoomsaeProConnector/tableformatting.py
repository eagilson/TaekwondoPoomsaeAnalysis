import pandas as pd
from datetime import date
from utils import insert_contiguous_columns

def formatPP_Scores(data: list, DatabaseID: str, tablename: str, event: str, start_date: date, databasename: str, column_count: int) -> list:
    """
    Formats data from the various Poomsae Pro database versions.

    Args:
        data (List[Row]): Single Table data from the source database.
        DatabaseID (int): Unique Identifier of the source database.
        tablename (str): Table in database being formatted.
        event (str): Name of the event.
        start_date (date): Start date of the event.
        databasename (str): Original file name of the Poomsae Pro database. This gives the relevant version.
        column_count (int): Count of columns in the table to be formatted.
        
    Returns:
        datawid (List): Formatted single table data.
    """


    #format data to match current tables
    #generall formatting
    #adds the DatabaseID for data consistenty
    datawid = [(DatabaseID,) + tuple(row) for row in data]
    #remove the NONE values and Python doesn't like them
    datawid = [tuple('None' if x is None else x for x in t) for t in datawid]
    #update all datetime functions
    datawid = [tuple(item.strftime('%Y-%m-%d') if isinstance(item, date) else item for item in t) for t in datawid]

    match tablename:
        case 'SportSettings':
            datawid = formatSportSettings(datawid, databasename)
        case 'DivisionNames':
            datawid = formatDivisionNames(datawid, databasename, event)
        case 'SEMatchList':
            datawid = formatSEMatchList(datawid, databasename, start_date)
        case 'CategoryTbl':
            datawid = formatCategoryTbl(datawid, databasename)

    #update data to match column count
    datawid = [tuple(list(t) + [0] * (column_count - len(t))) for t in datawid]

    #inserts into the master database
    return datawid

def formatSportSettings(datawid, databasename):

    match databasename:
        case 'PP_ScoresV2c.accdb':
            #code to account for added field in V3c on SportSettings
            df = pd.DataFrame(datawid)
            df.insert(loc=4, column='Rev',value='PP_V2c')
            datawid = [tuple(row) for row in df.to_numpy()]
        case 'PP_ScoresV1c.accdb':
            #code to account for added field in V3c on SportSettings
            df = pd.DataFrame(datawid)
            df.insert(loc=4, column='Rev',value='PP_V1c')
            datawid = [tuple(row) for row in df.to_numpy()]
        case 'PP_ScoresV4t.accdb':
            #code to account for updated fields
            df = pd.DataFrame(datawid)
            df.insert(loc=4, column='Rev',value='PP_V4t')
            df.insert(loc=6, column='MaxPoomsaeTime',value=0)
            df.insert(loc=8, column='MinPoomsaeTime',value=0)
            #Radio2FinalScoreRandom & Date2use switched
            #RadioPrelim1Form Boolean NOT NULL, 
            #RadioPrelim2Form Boolean NOT NULL, 
            #RadioSemi1Form Boolean NOT NULL, 
            #RadioSemi2Form Boolean NOT NULL, 
            #RadioFinal1Form Boolean NOT NULL, 
            #RadioFinal2Form Boolean NOT NULL, 
            #RadioBracket1Form Boolean NOT NULL, 
            #RadioBracket2Form Boolean NOT NULL, 
            #FinalBrackSeeding INTEGER, 
            #DisplayAllJudgesB4Display Boolean NOT NULL, 
            #datawid = [tuple(row) for row in df.to_numpy()]

            #Ignore sport settings for now
            datawid.clear

    return datawid

def formatDivisionNames(datawid, databasename, event):
    # CHANGE LIST FOR DB VERSIONS
    # V3c Changed the column order 
    ## Columns CompMth_Black & CompOrder added
    ## Poomsae draw added as separate columns for each belt
    # V4c moved the poomsae draw to PoomsaePreset table
    ## Removed all belt specific poomsae draw columns
    ## Added CompMeth for Yellow through Red
    ## Added default Poomsae for each round for draw setup

    df = pd.DataFrame(datawid)

    #V3c Changes
    match databasename:
        case 'PP_ScoresV1c.accdb':
            df['CompMth_Black'] = df.iloc[:,6]
            df['CompOrder'] = df.iloc[:,4]
            df = df.iloc[:,[0,1,2,3,9,8,6,4,5]]
        case 'PP_ScoresV2c.accdb':
            #This doesn't work for 2025 Team Trials
            if event != '2025 USATKD Team Trials':
                df['CompMth_Black'] = df.iloc[:,6]
                df['CompOrder'] = df.iloc[:,4]
                df = df.iloc[:,[0,1,2,3,9,8,6,4,5,7]]
    
    #V4c Changes
    match databasename:        
        case 'PP_ScoresV1c.accdb' | 'PP_ScoresV2c.accdb' | 'PP_ScoresV3c.accdb':
            # New CompMeth columns
            CompMeth_Columns = ['CompMeth_Red', 'CompMeth_Blue', 'CompMeth_Green', 'CompMeth_Yellow']
            df = insert_contiguous_columns(df, 6, CompMeth_Columns)
            #df.insert(loc=7, column='CompMeth_Red',value='')
            #df.insert(loc=8, column='CompMeth_Blue',value='')
            #df.insert(loc=9, column='CompMeth_Green',value='')
            #df.insert(loc=10, column='CompMeth_Yellow',value='')
            
            # New Detault columns
            Default_Columns = [
                'DefaultR2P1',
                'DefaultR2P2',
                'DefaultR2Sim',
                'DefaultR4P1',
                'DefaultR4P2',
                'DefaultR4Sim',
                'DefaultR8P1',
                'DefaultR8P2',
                'DefaultR8Sim',
                'DefaultR16P1',
                'DefaultR16P2',
                'DefaultR16Sim',
                'DefaultR32P1',
                'DefaultR32P2',
                'DefaultR32Sim',
                'DefaultR64P1',
                'DefaultR64P2',
                'DefaultR64Sim',
                'DefaultR128P1',
                'DefaultR128P2',
                'DefaultR128Sim'
            ]
            fill_values = {
                'DefaultR2P1': '', 
                'DefaultR2P2': '', 
                'DefaultR2Sim': False,
                'DefaultR4P1': '', 
                'DefaultR4P2': '',
                'DefaultR4Sim': False,
                'DefaultR8P1': '',
                'DefaultR8P2': '',
                'DefaultR8Sim': False,
                'DefaultR16P1': '',
                'DefaultR16P2': '',
                'DefaultR16Sim': False,
                'DefaultR32P1': '',
                'DefaultR32P2': '',
                'DefaultR32Sim': False,
                'DefaultR64P1': '',
                'DefaultR64P2': '',
                'DefaultR64Sim': False,
                'DefaultR128P1': '',
                'DefaultR128P2': '',
                'DefaultR128Sim': False
            }
            df = insert_contiguous_columns(df, 12, Default_Columns, fill_values)


        case 'PP_ScoresV4c.accdb':
            # Old CompMeth columns
            df.insert(loc=10, column='CompMeth_Color',value='')

    datawid = [tuple(row) for row in df.to_numpy()]

    return datawid

def formatSEMatchList(datawid, databasename, start_date):
    # CHANGE LIST FOR DB VERSIONS
    # V3c update on 2025-07
    ## Added NextMatch & Breaking Columns
    # V4c adds columns and changes column order
    ## Added ChungCheck, HongCheck, RingNo, RingOrder 
    ## Removed NextMatch
    ## Columns added between Breakind and Gender

    df = pd.DataFrame(datawid)

    match databasename:
        case 'PP_ScoresV3c.accdb':
            #SEMatchList table missing NextMatch & Breaking columns
            if start_date < '2025-07-01':
                df.insert(loc=3, column='NextMatch',value='')
                df.insert(loc=4, column='Breaking',value=False)

            # account for ChungCheck, HongCheck, RingNo, RingOrder        
            df.insert(loc=5, column='ChungCheck',value=False)
            df.insert(loc=6, column='HongCheck',value=False)
            df.insert(loc=7, column='RingNo',value='')
            df.insert(loc=8, column='RingOrder',value='')

        case 'PP_ScoresV4c.accdb':
            # account for removed NextMatch Column
            df.insert(loc=3, column='NextMatch',value='')

    datawid = [tuple(row) for row in df.to_numpy()]
    
    return datawid

def formatCategoryTbl(datawid, databasename):
    # CHANGE LIST FOR DB VERSIONS
    # V4c adds defaults for Poomsae and Simultaneous
    ## This does not require custom code as it is handled by the generic padder

    return datawid