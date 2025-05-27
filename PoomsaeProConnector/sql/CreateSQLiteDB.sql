--DROP TABLE need one for each table to reset database
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS CompMethod;
DROP TABLE IF EXISTS Gender;
DROP TABLE IF EXISTS BCategory;
DROP TABLE IF EXISTS BDivisionNames;
DROP TABLE IF EXISTS BreakingScores;
DROP TABLE IF EXISTS BreakingSettings;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Color;
DROP TABLE IF EXISTS Competitors;
DROP TABLE IF EXISTS DivisionNames;
DROP TABLE IF EXISTS Event_Info;
DROP TABLE IF EXISTS IndPoomsaeScores;
DROP TABLE IF EXISTS IndPoomsaeScoresDetails;
DROP TABLE IF EXISTS IndTotalScores;
DROP TABLE IF EXISTS Judges;
DROP TABLE IF EXISTS Poomsae;
DROP TABLE IF EXISTS PoomsaeScores;
DROP TABLE IF EXISTS Rank;
DROP TABLE IF EXISTS Round;
DROP TABLE IF EXISTS Schools;
DROP TABLE IF EXISTS ScoreDetails;
DROP TABLE IF EXISTS SportSettings;
DROP TABLE IF EXISTS TTDivisionNames;
DROP TABLE IF EXISTS TTRound;

--Comp Method
CREATE TABLE IF NOT EXISTS CompMethod (
    DatabaseID INTEGER NOT NULL,
    CompMethodID INTEGER,
    CompMethod TEXT NOT NULL,
    PRIMARY KEY (DatabaseID, CompMethodID)
) WITHOUT ROWID;

--Comp Method has fixed values
/* INSERT INTO CompMethod(CompMethodID, CompMethod)
VALUES
    (1, "Single Elimination"),
    (2, "Round Robin"),
    (3, "Cut off"),
    (4, "Combination: Cut off + Elimination")
ON CONFLICT (CompMethodID)
DO NOTHING */

--Gender
CREATE TABLE IF NOT EXISTS Gender (
    DatabaseID INTEGER NOT NULL,
    Gender_ID INTEGER,
    Gender TEXT NOT NULL,
    PRIMARY KEY (DatabaseID, Gender_ID)
) WITHOUT ROWID;

--Gender has fixed values
/* INSERT INTO Gender(Gender_ID, Gender)
VALUES
    (1, "Male"),
    (2, "Female"),
    (3, "Mixed")
ON CONFLICT (Gender_ID)
DO NOTHING */

--Event
CREATE TABLE IF NOT EXISTS Events (
    DatabaseID INTEGER NOT NULL,
    EventName TEXT NOT NULL,
    CompDay INTEGER,
    Ring TEXT,
    StartDate DATE,
    EndDate DATE,
    DatabaseName TEXT NOT NULL,
    PRIMARY KEY (DatabaseID, EventName,CompDay,Ring)    
) WITHOUT ROWID;

--BCategory
CREATE TABLE IF NOT EXISTS  BCategory
 (
    DatabaseID INTEGER NOT NULL,
	Category_ID Integer, 
	Category Text NOT NULL,
    PRIMARY KEY (DatabaseID, Category_ID)
) WITHOUT ROWID;

--BDivision Names
CREATE TABLE IF NOT EXISTS BDivisionNames
 (
    DatabaseID INTEGER NOT NULL,
	Division_ID Integer, 
	Division Text NOT NULL, 
	FixedDivision Boolean NOT NULL, 
	AgeStart Integer, 
	AgeEnd Integer,
    PRIMARY KEY (DatabaseID, Division_ID)
) WITHOUT ROWID;

--Breaking Scores
CREATE TABLE BreakingScores
 (
    DatabaseID INTEGER NOT NULL,
	Performance_ID Integer NOT NULL, 
	RingNbr Integer, 
	SelectRecord Boolean NOT NULL, 
	Selected4Sort Text, 
	OrderOfPerform Integer, 
	CompetitorNbr Integer NOT NULL, 
	Division Integer NOT NULL, 
	Gender Integer NOT NULL, 
	Category Integer NOT NULL, 
	Status Integer NOT NULL, 
	Placement Integer, 
	NumberOfBoards Integer, 
	ValueOfBoards Numeric, 
	Technical_Penalty Numeric, 
	Technical_val_min Numeric, 
	Technical_val_maj Numeric, 
	Technical_numb_min Integer, 
	Technical_numb_maj Integer, 
	Difficulty_R Numeric, 
	Difficulty_J1 Numeric, 
	Difficulty_J2 Numeric, 
	Difficulty_J3 Numeric, 
	Difficulty_J4 Numeric, 
	Difficulty_Avg Numeric, 
	Technical_Score Numeric, 
	Override_R Boolean NOT NULL, 
	Override_J1 Boolean NOT NULL, 
	Override_J2 Boolean NOT NULL, 
	Override_J3 Boolean NOT NULL, 
	Override_J4 Boolean NOT NULL, 
	Pre_R Numeric, 
	Pre_J1 Numeric, 
	Pre_J2 Numeric, 
	Pre_J3 Numeric, 
	Pre_J4 Numeric, 
	Pre_Avg Numeric, 
	Time_Penalty_Seconds Integer, 
	Proc_Penalty Numeric, 
	SubTotal Numeric, 
	Breaking_Score Numeric NOT NULL, 
	Total_Score Numeric, 
	Pre_R_Q1 Numeric, 
	Pre_R_Q2 Numeric, 
	Pre_R_Q3 Numeric, 
	Pre_R_Q4 Numeric, 
	Pre_J1_Q1 Numeric, 
	Pre_J1_Q2 Numeric, 
	Pre_J1_Q3 Numeric, 
	Pre_J1_Q4 Numeric, 
	Pre_J2_Q1 Numeric, 
	Pre_J2_Q2 Numeric, 
	Pre_J2_Q3 Numeric, 
	Pre_J2_Q4 Numeric, 
	Pre_J3_Q1 Numeric, 
	Pre_J3_Q2 Numeric, 
	Pre_J3_Q3 Numeric, 
	Pre_J3_Q4 Numeric, 
	Pre_J4_Q1 Numeric, 
	Pre_J4_Q2 Numeric, 
	Pre_J4_Q3 Numeric, 
	Pre_J4_Q4 Numeric,
    PRIMARY KEY (DatabaseID, Performance_ID)
) WITHOUT ROWID;

--BreakingSettings
CREATE TABLE IF NOT EXISTS BreakingSettings
 (
    DatabaseID INTEGER NOT NULL,
	ID Integer NOT NULL, 
	Active Boolean NOT NULL, 
	ProfileName Text, 
	PerformanceTIme Integer, 
	Date2use DateTime, 
	EndOfYear Boolean NOT NULL, 
	DisplayBetweenComps Integer, 
	DisplayBetweenDivs Integer, 
	AudTransformX REAL, 
	AudTransformY REAL, 
	AdmTransformX REAL, 
	AdmTransformY REAL, 
	TimeToDisplayScores Integer, 
	EventYear Text, 
	EventName Text,
    PRIMARY KEY (DatabaseID, ID)
) WITHOUT ROWID;

--Category
CREATE TABLE IF NOT EXISTS Category
 (
    DatabaseID INTEGER NOT NULL,
	Category_ID Integer, 
	Category Text NOT NULL, 
	Range_Min Integer, 
	Range_Max Integer,
    PRIMARY KEY (DatabaseID, Category_ID)
) WITHOUT ROWID;

--Color
CREATE TABLE IF NOT EXISTS Color
 (
    DatabaseID INTEGER NOT NULL,
	Color_ID text NOT NULL, 
	Color Text,
    PRIMARY KEY (DatabaseID, Color_ID)
) WITHOUT ROWID;

--Competitors
CREATE TABLE IF NOT EXISTS Competitors
 (
    DatabaseID INTEGER NOT NULL,
	Comp_ID Integer, 
	Comp_Number Integer NOT NULL, 
	Membership_Numb Text, 
	Select_Comp_record Boolean NOT NULL, 
	Comp_Title Text, 
	Comp_First Text NOT NULL, 
	Comp_Middle Text, 
	Comp_Last Text NOT NULL, 
	Comp_Suffix Text, 
	Comp_DOB DateTime, 
	Comp_Gender Integer, 
	Comp_Rank_Level Integer, 
	Comp_Rank_Color Integer, 
	Comp_Town Text, 
	Comp_State Text, 
	Comp_Country Text, 
	Comp_School Integer, 
	Poomsae_Div Text, 
	Freestyle_Div Text, 
	Breaking_Div Text, 
	Seeding Integer,
    PRIMARY KEY (DatabaseID, Comp_ID)
) WITHOUT ROWID;

--Division Names
CREATE TABLE IF NOT EXISTS DivisionNames
 (
    DatabaseID INTEGER NOT NULL,
	Division_ID Integer, 
	Division Text NOT NULL, 
	FixedDivision Boolean NOT NULL, 
	CompOrder Integer, 
	CompMeth_Black Integer, 
	CompMeth_Color Integer, 
	Range_Min Integer, 
	Range_Max Integer, 
	MaleYellowPrelim Integer, 
	MaleYellowSemi Integer, 
	MaleYellowFinal1 Integer, 
	MaleYellowFinal2 Integer, 
	FemaleYellowPrelim Integer, 
	FemaleYellowSemi Integer, 
	FemaleYellowFinal1 Integer, 
	FemaleYellowFinal2 Integer, 
	MaleGreenPrelim Integer, 
	MaleGreenSemi Integer, 
	MaleGreenFinal1 Integer, 
	MaleGreenFinal2 Integer, 
	FemaleGreenPrelim Integer, 
	FemaleGreenSemi Integer, 
	FemaleGreenFinal1 Integer, 
	FemaleGreenFinal2 Integer, 
	MaleBluePrelim Integer, 
	MaleBlueSemi Integer, 
	MaleBlueFinal1 Integer, 
	MaleBlueFinal2 Integer, 
	FemaleBluePrelim Integer, 
	FemaleBlueSemi Integer, 
	FemaleBlueFinal1 Integer, 
	FemaleBlueFinal2 Integer, 
	MaleRedPrelim Integer, 
	MaleRedSemi Integer, 
	MaleRedFinal1 Integer, 
	MaleRedFinal2 Integer, 
	FemaleRedPrelim Integer, 
	FemaleRedSemi Integer, 
	FemaleRedFinal1 Integer, 
	FemaleRedFinal2 Integer, 
	Ro2Male1 Integer, 
	Ro2Male2 Integer, 
	Ro2Female1 Integer, 
	Ro2Female2 Integer, 
	Ro4Male1 Integer, 
	Ro4Male2 Integer, 
	Ro4Female1 Integer, 
	Ro4Female2 Integer, 
	Ro8Male1 Integer, 
	Ro8Male2 Integer, 
	Ro8Female1 Integer, 
	Ro8Female2 Integer, 
	Ro16Male1 Integer, 
	Ro16Male2 Integer, 
	Ro16Female1 Integer, 
	Ro16Female2 Integer, 
	Ro32Male1 Integer, 
	Ro32Male2 Integer, 
	Ro32Female1 Integer, 
	Ro32Female2 Integer, 
	Ro64Male1 Integer, 
	Ro64Male2 Integer, 
	Ro64Female1 Integer, 
	Ro64Female2 Integer, 
	Ro128Male1 Integer, 
	Ro128Male2 Integer, 
	Ro128Female1 Integer, 
	Ro128Female2 Integer, 
	Ro2MaleSimul Boolean NOT NULL, 
	Ro2FemaleSimul Boolean NOT NULL, 
	Ro4MaleSimul Boolean NOT NULL, 
	Ro4FemaleSimul Boolean NOT NULL, 
	Ro8MaleSimul Boolean NOT NULL, 
	Ro8FemaleSimul Boolean NOT NULL, 
	Ro16MaleSimul Boolean NOT NULL, 
	Ro16FemaleSimul Boolean NOT NULL, 
	Ro32MaleSimul Boolean NOT NULL, 
	Ro32FemaleSimul Boolean NOT NULL, 
	Ro64MaleSimul Boolean NOT NULL, 
	Ro64FemaleSimul Boolean NOT NULL, 
	Ro128MaleSimul Boolean NOT NULL, 
	Ro128FemaleSimul Boolean NOT NULL,
    PRIMARY KEY (DatabaseID, Division_ID)
) WITHOUT ROWID;

--Event_Info
CREATE TABLE IF NOT EXISTS Event_Info
 (
    DatabaseID INTEGER NOT NULL,
	Event_ID Integer, 
	EventName Text NOT NULL, 
	EventDate DateTime, 
	EventLocation Text, 
	EventAddress Text, 
	EventCity Text, 
	EventState Text, 
	EventZip Text, 
	EventHost Text, 
	EventLogo TEXT,
    PRIMARY KEY (DatabaseID, Event_ID)
) WITHOUT ROWID;

--Ind Poomsae Socres
CREATE TABLE IF NOT EXISTS IndPoomsaeScores
 (
    DatabaseID INTEGER NOT NULL,
	Performance_ID Integer NOT NULL, 
	RingNbr Integer, 
	SelectRecord Boolean NOT NULL, 
	Selected4Sort Text, 
	OrderOfPerform Integer, 
	CompetitorNbr Integer NOT NULL, 
	RoundName Integer NOT NULL, 
	Division Integer NOT NULL, 
	Gender Integer NOT NULL, 
	Category Integer NOT NULL, 
	Status Integer NOT NULL, 
	Placement Integer, 
	FormName_A Text, 
	Acc_R_A Numeric, 
	Acc_J1_A Numeric, 
	Acc_J2_A Numeric, 
	Acc_J3_A Numeric, 
	Acc_J4_A Numeric, 
	Acc_J5_A Numeric, 
	Acc_J6_A Numeric, 
	Acc_Avg_A Numeric, 
	Pre_R_A Numeric, 
	Pre_J1_A Numeric, 
	Pre_J2_A Numeric, 
	Pre_J3_A Numeric, 
	Pre_J4_A Numeric, 
	Pre_J5_A Numeric, 
	Pre_J6_A Numeric, 
	Pre_Avg_A Numeric, 
	Override_R_A Boolean NOT NULL, 
	Override_J1_A Boolean NOT NULL, 
	Override_J2_A Boolean NOT NULL, 
	Override_J3_A Boolean NOT NULL, 
	Override_J4_A Boolean NOT NULL, 
	Override_J5_A Boolean NOT NULL, 
	Override_J6_A Boolean NOT NULL, 
	Pen_OT_A Numeric, 
	Pen_OOB_A Numeric, 
	Form_Score_A Numeric, 
	Form_Score_AB Numeric, 
	Presentation_Total Numeric, 
	Full_Score Numeric, 
	TieBreaker_Score Numeric, 
	TieBreaker_Total Numeric, 
	TieBreaker_needed Text, 
	FormName_T Text, 
	Acc_R_T Numeric, 
	Acc_J1_T Numeric, 
	Acc_J2_T Numeric, 
	Acc_J3_T Numeric, 
	Acc_J4_T Numeric, 
	Acc_J5_T Numeric, 
	Acc_J6_T Numeric, 
	Acc_Avg_T Numeric, 
	Pre_R_T Numeric, 
	Pre_J1_T Numeric, 
	Pre_J2_T Numeric, 
	Pre_J3_T Numeric, 
	Pre_J4_T Numeric, 
	Pre_J5_T Numeric, 
	Pre_J6_T Numeric, 
	Pre_Avg_T Numeric, 
	Override_R_T Boolean NOT NULL, 
	Override_J1_T Boolean NOT NULL, 
	Override_J2_T Boolean NOT NULL, 
	Override_J3_T Boolean NOT NULL, 
	Override_J4_T Boolean NOT NULL, 
	Override_J5_T Boolean NOT NULL, 
	Override_J6_T Boolean NOT NULL, 
	Pen_OT_T Numeric, 
	Pen_OOB_T Numeric,
    PRIMARY KEY (DatabaseID, Performance_ID)
) WITHOUT ROWID;

--Ind Poomsae Socres Details
CREATE TABLE IF NOT EXISTS IndPoomsaeScoresDetails
 (
    DatabaseID INTEGER NOT NULL,
	Performance_Details_ID Integer NOT NULL, 
	Performance_ID Integer NOT NULL, 
	Acc_R_A_min Integer, 
	Acc_R_A_maj Integer, 
	Acc_J1_A_min Integer, 
	Acc_J1_A_maj Integer, 
	Acc_J2_A_min Integer, 
	Acc_J2_A_maj Integer, 
	Acc_J3_A_min Integer, 
	Acc_J3_A_maj Integer, 
	Acc_J4_A_min Integer, 
	Acc_J4_A_maj Integer, 
	Acc_J5_A_min Integer, 
	Acc_J5_A_maj Integer, 
	Acc_J6_A_min Integer, 
	Acc_J6_A_maj Integer, 
	Pre_R_A_Q1 Numeric, 
	Pre_R_A_Q2 Numeric, 
	Pre_R_A_Q3 Numeric, 
	Pre_J1_A_Q1 Numeric, 
	Pre_J1_A_Q2 Numeric, 
	Pre_J1_A_Q3 Numeric, 
	Pre_J2_A_Q1 Numeric, 
	Pre_J2_A_Q2 Numeric, 
	Pre_J2_A_Q3 Numeric, 
	Pre_J3_A_Q1 Numeric, 
	Pre_J3_A_Q2 Numeric, 
	Pre_J3_A_Q3 Numeric, 
	Pre_J4_A_Q1 Numeric, 
	Pre_J4_A_Q2 Numeric, 
	Pre_J4_A_Q3 Numeric, 
	Pre_J5_A_Q1 Numeric, 
	Pre_J5_A_Q2 Numeric, 
	Pre_J5_A_Q3 Numeric, 
	Pre_J6_A_Q1 Numeric, 
	Pre_J6_A_Q2 Numeric, 
	Pre_J6_A_Q3 Numeric, 
	Acc_R_T_min Integer, 
	Acc_R_T_maj Integer, 
	Acc_J1_T_min Integer, 
	Acc_J1_T_maj Integer, 
	Acc_J2_T_min Integer, 
	Acc_J2_T_maj Integer, 
	Acc_J3_T_min Integer, 
	Acc_J3_T_maj Integer, 
	Acc_J4_T_min Integer, 
	Acc_J4_T_maj Integer, 
	Acc_J5_T_min Integer, 
	Acc_J5_T_maj Integer, 
	Acc_J6_T_min Integer, 
	Acc_J6_T_maj Integer,
    PRIMARY KEY (DatabaseID, Performance_ID,Performance_Details_ID)
) WITHOUT ROWID;

--Ind Total Scores
CREATE TABLE IF NOT EXISTS IndTotalScores
 (
    DatabaseID INTEGER NOT NULL,
	Ind_Total_ID Integer NOT NULL, 
	SelectRecord Boolean NOT NULL, 
	Selected4Sort Text, 
	OrderOfPerform Integer, 
	Placement Integer, 
	CompetitorNbr Integer NOT NULL, 
	Division Integer NOT NULL, 
	Gender Integer NOT NULL, 
	Category Integer NOT NULL, 
	Total_Score Numeric, 
	Total_Presentation Numeric, 
	Total_Total Numeric, 
	Total_TB Numeric, 
	Total_TB_Total Numeric, 
	TieBreaker_needed Text, 
	Round1_Score Numeric NOT NULL, 
	Round1_Presentation Numeric, 
	Round1_Total Numeric, 
	Round1_TB Numeric, 
	Round1_TB_Total Numeric, 
	Round1_Form Text, 
	Round1_Placement Integer, 
	Round2_Score Numeric NOT NULL, 
	Round2_Presentation Numeric, 
	Round2_Total Numeric, 
	Round2_TB Numeric, 
	Round2_TB_Total Numeric, 
	Round2_Form Text, 
	Round2_Placement Integer, 
	Round3_Score Numeric NOT NULL, 
	Round3_Presentation Numeric, 
	Round3_Total Numeric, 
	Round3_TB Numeric, 
	Round3_TB_Total Numeric, 
	Round3_Form Text, 
	Round3_Placement Integer, 
	Round4_Score Numeric NOT NULL, 
	Round4_Presentation Numeric, 
	Round4_Total Numeric, 
	Round4_TB Numeric, 
	Round4_TB_Total Numeric, 
	Round4_Form Text, 
	Round4_Placement Integer, 
	Round5_Score Numeric NOT NULL, 
	Round5_Presentation Numeric, 
	Round5_Total Numeric, 
	Round5_TB Numeric, 
	Round5_TB_Total Numeric, 
	Round5_Form Text, 
	Round5_Placement Integer, 
	Round6_Score Numeric NOT NULL, 
	Round6_Presentation Numeric, 
	Round6_Total Numeric, 
	Round6_TB Numeric, 
	Round6_TB_Total Numeric, 
	Round6_Form Text, 
	Round6_Placement Integer, 
	Round7_Score Numeric NOT NULL, 
	Round7_Presentation Numeric, 
	Round7_Total Numeric, 
	Round7_TB Numeric, 
	Round7_TB_Total Numeric, 
	Round7_Form Text, 
	Round7_Placement Integer, 
	Round8_Score Numeric NOT NULL, 
	Round8_Presentation Numeric, 
	Round8_Total Numeric, 
	Round8_TB Numeric, 
	Round8_TB_Total Numeric, 
	Round8_Form Text, 
	Round8_Placement Integer, 
	Tiebreaker_Score Numeric NOT NULL, 
	Tiebreaker_Presentation Numeric, 
	Tiebreaker_Total Numeric, 
	Tiebreaker_TB Numeric, 
	Tiebreaker_TB_Total Numeric, 
	Tiebreaker_Form Text, 
	FirstPlace Integer, 
	SecondPlace Integer, 
	ThirdPlace Integer, 
	FourthPlace Integer, 
	FifthPlace Integer, 
	SixthPlace Integer, 
	SeventhPlace Integer, 
	EighthPlace Integer,
    PRIMARY KEY (DatabaseID, Ind_Total_ID)
) WITHOUT ROWID;

--Judges
CREATE TABLE IF NOT EXISTS Judges
 (
    DatabaseID INTEGER NOT NULL,
	Judge_ID Integer NOT NULL, 
	Judge_Title Text, 
	Judge_First Text NOT NULL, 
	Judge_Middle Text, 
	Judge_Last Text NOT NULL, 
	Judge_Suffix Text, 
	Judge_State_NOC Text, 
	Judge_Level Text, 
	Judge_USATKD Text, 
	Judge_CurRing Integer,
    PRIMARY KEY (DatabaseID, Judge_ID)
) WITHOUT ROWID;

--Poomsae
CREATE TABLE IF NOT EXISTS Poomsae
 (
    DatabaseID INTEGER NOT NULL,
	Poomsae_ID Integer, 
	Poomsae Text,
    PRIMARY KEY (DatabaseID, Poomsae_ID)
) WITHOUT ROWID;

--Poomsae Scores
CREATE TABLE IF NOT EXISTS PoomsaeScores
 (
    DatabaseID INTEGER NOT NULL,
	Performance_ID Integer NOT NULL, 
	RingNbr Integer, 
	SelectRecord Boolean NOT NULL, 
	Selected4Sort Text, 
	OrderOfPerform Integer, 
	CompetitorNbr Integer NOT NULL, 
	RoundName Integer NOT NULL, 
	Division Integer NOT NULL, 
	Gender Integer NOT NULL, 
	Category Integer NOT NULL, 
	Status Integer NOT NULL, 
	Placement Integer, 
	FormName_A Text, 
	Acc_R_A Numeric, 
	Acc_J1_A Numeric, 
	Acc_J2_A Numeric, 
	Acc_J3_A Numeric, 
	Acc_J4_A Numeric, 
	Acc_J5_A Numeric, 
	Acc_J6_A Numeric, 
	Acc_Avg_A Numeric, 
	Pre_R_A Numeric, 
	Pre_J1_A Numeric, 
	Pre_J2_A Numeric, 
	Pre_J3_A Numeric, 
	Pre_J4_A Numeric, 
	Pre_J5_A Numeric, 
	Pre_J6_A Numeric, 
	Pre_Avg_A Numeric, 
	Override_R_A Boolean NOT NULL, 
	Override_J1_A Boolean NOT NULL, 
	Override_J2_A Boolean NOT NULL, 
	Override_J3_A Boolean NOT NULL, 
	Override_J4_A Boolean NOT NULL, 
	Override_J5_A Boolean NOT NULL, 
	Override_J6_A Boolean NOT NULL, 
	Pen_OT_A Numeric, 
	Pen_OOB_A Numeric, 
	Form_Score_A Numeric, 
	FormName_B Text, 
	Acc_R_B Numeric, 
	Acc_J1_B Numeric, 
	Acc_J2_B Numeric, 
	Acc_J3_B Numeric, 
	Acc_J4_B Numeric, 
	Acc_J5_B Numeric, 
	Acc_J6_B Numeric, 
	Acc_Avg_B Numeric, 
	Pre_R_B Numeric, 
	Pre_J1_B Numeric, 
	Pre_J2_B Numeric, 
	Pre_J3_B Numeric, 
	Pre_J4_B Numeric, 
	Pre_J5_B Numeric, 
	Pre_J6_B Numeric, 
	Pre_Avg_B Numeric, 
	Override_R_B Boolean NOT NULL, 
	Override_J1_B Boolean NOT NULL, 
	Override_J2_B Boolean NOT NULL, 
	Override_J3_B Boolean NOT NULL, 
	Override_J4_B Boolean NOT NULL, 
	Override_J5_B Boolean NOT NULL, 
	Override_J6_B Boolean NOT NULL, 
	Pen_OT_B Numeric, 
	Pen_OOB_B Numeric, 
	Form_Score_B Numeric, 
	Form_Score_AB Numeric, 
	Presentation_Total Numeric, 
	Full_Score Numeric, 
	TieBreaker_Score Numeric, 
	TieBreaker_Total Numeric, 
	TieBreaker_needed Text, 
	FormName_T Text, 
	Acc_R_T Numeric, 
	Acc_J1_T Numeric, 
	Acc_J2_T Numeric, 
	Acc_J3_T Numeric, 
	Acc_J4_T Numeric, 
	Acc_J5_T Numeric, 
	Acc_J6_T Numeric, 
	Acc_Avg_T Numeric, 
	Pre_R_T Numeric, 
	Pre_J1_T Numeric, 
	Pre_J2_T Numeric, 
	Pre_J3_T Numeric, 
	Pre_J4_T Numeric, 
	Pre_J5_T Numeric, 
	Pre_J6_T Numeric, 
	Pre_Avg_T Numeric, 
	Override_R_T Boolean NOT NULL, 
	Override_J1_T Boolean NOT NULL, 
	Override_J2_T Boolean NOT NULL, 
	Override_J3_T Boolean NOT NULL, 
	Override_J4_T Boolean NOT NULL, 
	Override_J5_T Boolean NOT NULL, 
	Override_J6_T Boolean NOT NULL, 
	Pen_OT_T Numeric, 
	Pen_OOB_T Numeric,
    PRIMARY KEY (DatabaseID, Performance_ID)
) WITHOUT ROWID;

--Rank
CREATE TABLE IF NOT EXISTS Rank
 (
    DatabaseID INTEGER NOT NULL,
	Rank_ID Integer, 
	Rank Text,
    PRIMARY KEY (DatabaseID, Rank_ID)
) WITHOUT ROWID;

--Round
CREATE TABLE IF NOT EXISTS Round
 (
    DatabaseID INTEGER NOT NULL,
	Round_ID Integer, 
	Round Text NOT NULL,
    PRIMARY KEY (DatabaseID, Round_ID)
) WITHOUT ROWID;

--Schools
CREATE TABLE IF NOT EXISTS Schools
 (
    DatabaseID INTEGER NOT NULL,
	School_ID Integer, 
	SchoolName Text NOT NULL, 
	SchoolAddress Text, 
	SchoolAddress2 Text, 
	SchoolCity Text, 
	SchoolState Text, 
	SchoolZip Text, 
	SchoolPhone Text, 
	SchoolMasterInstructor Text,
    PRIMARY KEY (DatabaseID, School_ID)
) WITHOUT ROWID;

--Score Details
/* CREATE TABLE IF NOT EXISTS ScoreDetails
 (
    DatabaseID INTEGER NOT NULL,
	Performance_ID Integer NOT NULL, 
	Comp_Oper Text, 
	Coordinator Integer, 
	R_Judge Integer, 
	R_P1_AccTech Text, 
	R_P1_Pres Text, 
	R_P2_AccTech Text, 
	R_P2_Pres Text, 
	R_TB_AccTech Text, 
	R_TB_Pres Text, 
	J1_Judge Integer, 
	J1_P1_AccTech Text, 
	J1_P1_Pres Text, 
	J1_P2_AccTech Text, 
	J1_P2_Pres Text, 
	J1_TB_AccTech Text, 
	J1_TB_Pres Text, 
	J2_Judge Integer, 
	J2_P1_AccTech Text, 
	J2_P1_Pres Text, 
	J2_P2_AccTech Text, 
	J2_P2_Pres Text, 
	J2_TB_AccTech Text, 
	J2_TB_Pres Text, 
	J3_Judge Integer, 
	J3_P1_AccTech Text, 
	J3_P1_Pres Text, 
	J3_P2_AccTech Text, 
	J3_P2_Pres Text, 
	J3_TB_AccTech Text, 
	J3_TB_Pres Text, 
	J4_Judge Integer, 
	J4_P1_AccTech Text, 
	J4_P1_Pres Text, 
	J4_P2_AccTech Text, 
	J4_P2_Pres Text, 
	J4_TB_AccTech Text, 
	J4_TB_Pres Text, 
	J5_Judge Integer, 
	J5_P1_AccTech Text, 
	J5_P1_Pres Text, 
	J5_P2_AccTech Text, 
	J5_P2_Pres Text, 
	J5_TB_AccTech Text, 
	J5_TB_Pres Text, 
	J6_Judge Integer, 
	J6_P1_AccTech Text, 
	J6_P1_Pres Text, 
	J6_P2_AccTech Text, 
	J6_P2_Pres Text, 
	J6_TB_AccTech Text, 
	J6_TB_Pres Text,
    PRIMARY KEY (DatabaseID, Performance_ID)
) WITHOUT ROWID */

--SportSettings
CREATE TABLE IF NOT EXISTS SportSettings
 (
    DatabaseID INTEGER NOT NULL,
	ID Integer, 
	Active Boolean NOT NULL, 
	ProfileName Text, 
	MaxPoomsaeTIme Integer NOT NULL, 
	PerformanceTIme Integer, 
	MinPoomsaeTime Integer NOT NULL, 
	RestPeriod Integer NOT NULL, 
	Num2Semi Integer, 
	Perc2Semi Integer, 
	Radio2SemiScoreDesc Boolean NOT NULL, 
	Radio2SemiScoreAsc Boolean NOT NULL, 
	Radio2SemiScorePrev Boolean NOT NULL, 
	Radio2SemiScoreRandom Boolean NOT NULL, 
	Num2Final Integer, 
	Perc2Final Integer, 
	Radio2FinalScoreDesc Boolean NOT NULL, 
	Radio2FinalScoreAsc Boolean NOT NULL, 
	Radio2FinalScorePrev Boolean NOT NULL, 
	Date2use DateTime, 
	Radio2FinalScoreRandom Boolean NOT NULL, 
	EndOfYear Boolean NOT NULL, 
	RadioPrelim1Form Boolean NOT NULL, 
	RadioPrelim2Form Boolean NOT NULL, 
	RadioSemi1Form Boolean NOT NULL, 
	RadioSemi2Form Boolean NOT NULL, 
	RadioFinal1Form Boolean NOT NULL, 
	RadioFinal2Form Boolean NOT NULL, 
	RadioBracket1Form Boolean NOT NULL, 
	RadioBracket2Form Boolean NOT NULL, 
	FinalBrackSeeding INTEGER, 
	DisplayAllJudgesB4Display Boolean NOT NULL, 
	DisplayBetweenComps Integer, 
	DisplayBetweenDivs Integer, 
	AudTransformX REAL, 
	AudTransformY REAL, 
	AdmTransformX REAL, 
	AdmTransformY REAL, 
	DisplayAll10Judges Boolean NOT NULL, 
	EventYear Text, 
	EventName Text,
    PRIMARY KEY (DatabaseID, ID)
) WITHOUT ROWID;


--TT Division Names
CREATE TABLE IF NOT EXISTS TTDivisionNames
 (
    DatabaseID INTEGER NOT NULL,
	Division_ID Integer, 
	Division Text NOT NULL, 
	FixedDivision Boolean NOT NULL, 
	AgeStart Integer, 
	AgeEnd Integer, 
	CompMeth Integer, 
	Seeding Integer,
    PRIMARY KEY (DatabaseID, Division_ID)
) WITHOUT ROWID;

--TT Round
CREATE TABLE IF NOT EXISTS TTRound
 (
    DatabaseID INTEGER NOT NULL,
	Round_ID Integer, 
	Round Text NOT NULL,
    PRIMARY KEY (DatabaseID, Round_ID)
) WITHOUT ROWID;