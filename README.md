# Project Objective

This project contains code to analyze Taekwondo Poomsae scores. It consolidates information from multiple events into a single sqlLite database for further analysis.

# Event Data

No event data is included in the Git repository. User can only utilize this repository to analyze data they legally possess.

The project assumes all the data is in a folder labeled data located in the root directory. The data folder contains a file called EVENTS.JSON detailing all events.

# Scoring Systems

Each Poomsae Scoring System utilized different database structures.  A separate connector to unify the data for analysis is required. 

## Poomsae Pro
The default import functionality assumes a PoomsaePro database. The PP_ScoresV2c.accdb and PP_ScoresV3c.accdb databases are currently supported. Support for earlier versions will be added as time permits.

Steps to build the PoomsaePro data for analysis:
1. PoomsaeProConnector/PoomsaeProConnection.py is used to build the database of scores
2. PoomsaeProConnector/PoomsaeProRefereeCreation.py is run to generate the excel file to record referee position.
3. PoomsaeProConnector/PoomsaeProRefereeImport.py is run to import the referee positions into the database.

# Competition Documentation

The LaTeX folder contains code to generate Official Assignment sheets for use at events. This requires compiling using LaTeX and a file titled logo.jpg added in the Image folder for the sheet being generated.