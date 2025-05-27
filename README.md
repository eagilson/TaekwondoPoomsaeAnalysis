This project contains code to analyze Taekwondo Poomsae scores. 

The default import functionality assumes a PoomsaePro database.

The project assumes all the data is in a folder labeled data.
The data folder contains a file called EVENTS.JSON detailing all events.

Steps to build the PoomsaePro data for analysis:
1. PoomsaeProConnector/PoomsaeProConnection.py is used to build the database of scores
2. is run to generate the excel file to record referee position.
3. PoomsaeProConnector/PoomsaeProRefereeImport.py is run to import the referee positions into the database.