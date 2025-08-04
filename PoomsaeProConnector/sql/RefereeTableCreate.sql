DROP TABLE IF EXISTS RefereeAssignment;

--Comp Method
CREATE TABLE IF NOT EXISTS RefereeAssignment (
    EventName TEXT NOT NULL,
    Division TEXT NOT NULL,
    Gender TEXT NOT NULL,
    Category TEXT NOT NULL,
    Round TEXT NOT NULL,
    RingNbr INTEGER NOT NULL,
    CompDay Text NOT NULL, --2025 Nationals
    MatchNumber TEXT,
    Position TEXT NOT NULL,
    RefereeName TEXT NOT NULL,
    PRIMARY KEY (EventName, Division, Gender, Category, Round, RingNbr, CompDay, MatchNumber, Position)
) WITHOUT ROWID;