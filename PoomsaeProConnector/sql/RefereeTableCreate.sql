DROP TABLE IF EXISTS RefereeAssignment;

--Comp Method
CREATE TABLE IF NOT EXISTS RefereeAssignment (
    EventName TEXT NOT NULL,
    Division TEXT NOT NULL,
    Gender TEXT NOT NULL,
    Category TEXT NOT NULL,
    Round TEXT NOT NULL,
    RingNbr INTEGER NOT NULL,
    MatchNumber TEXT,
    Position TEXT NOT NULL,
    RefereeName TEXT NOT NULL
);