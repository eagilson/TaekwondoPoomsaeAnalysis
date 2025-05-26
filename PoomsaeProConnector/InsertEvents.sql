INSERT INTO Events
    (DatabaseID,EventName,CompDay,Ring,StartDate,EndDate,DatabaseName)
VALUES
    (?,?,?,?,?,?,?)
ON CONFLICT (DatabaseID,EventName,CompDay,Ring)
DO NOTHING;
