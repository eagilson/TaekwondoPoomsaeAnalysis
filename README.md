# Project Objective

This project contains code to analyze Taekwondo Poomsae scores. It consolidates information from multiple events into a single sqlLite database for further analysis. 

# Event Data

No event data is included in the Git repository. User can only utilize this repository to analyze data they legally possess.

The project assumes all the data is in a folder labeled data located in the root directory. The data folder contains a file called EVENTS.JSON detailing all events.

# Technology Dependencies
Python
SQLlite
LaTeX


This project utilizes a Makefile to streamline data maintence and running the project. All dashboards can be run utilizing *make* commands. 

*make help* lists all available make commands.

# Referee Analysis

There are 3 dashboards to analyze referee performance.

## Referee Analysis

Running RefereeAnalysis.py generates a dashboard to examine individual referee's scoring. The dashboard has three tabs. 

1. **Referee Scoring Performance Dashboard** provides summary statistics for each referee aggregated at the event level.
2. **Score Detail** provides the score details used to compute the summary statistics.
3. **Score Difference** graphs the Accuracy and Presentation score differences.

## Single Elimination Consistency 

Running SingleEliminationConsistency.py generates a dashboard that provides the level of agreement between referees for Single Elimination rounds.

## Chung Sequential Advantage

Running ChungSequentialAdvantage.py generates a dashabord that evaluate if Chung has an advantage in Single Elimination Random Draw rounds contested sequentially instead of simultaneously. 

# Scoring Systems

Each Poomsae Scoring System utilized different database structures.  A separate connector to unify the data for analysis is required. 

## Poomsae Pro
The default import functionality assumes a PoomsaePro database. The PP_ScoresV2c.accdb and PP_ScoresV3c.accdb databases are currently supported. Support for earlier versions will be added as time permits.

Steps to build the PoomsaePro data for analysis:
1. Run *make poomsaepro-build* to create the databases and any missing referee assignment excel files
2. Populate the referee assignment excel files
3. Run *make referee-import* to import the referee assignments

If all referee assignment excel files are already populated, run *make poomsaepro-build-all* to build the database and import he referee assignments in one command.

# Competition Documentation

The LaTeX folder contains code to generate Official Assignment sheets for use at events. This requires compiling using LaTeX and a file titled logo.jpg added in the Image folder for the sheet being generated.
