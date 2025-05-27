SELECT DISTINCT
    D.Division,
    G.Gender,
    C.Category,
    R.Round,
    P.RingNbr
FROM 
    Events E,
    PoomsaeScores P,
    GenderTbl G,
    DivisionNames D,
    CategoryTbl C,
    RoundTbl R
WHERE
    E.DatabaseID = P.DatabaseID
    AND G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    AND D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    AND C.DatabaseID = E.DatabaseID AND P.Category = C.Category_ID
    AND R.DatabaseID = E.DatabaseID AND R.Round_ID = P.RoundName
    AND P.Acc_R_A <> -1
    AND E.EventName = :eventname
--Team Trials
UNION
SELECT DISTINCT
    D.Division,
    G.Gender,
    C.Category,
    R.Round,
    P.RingNbr
FROM 
    Events E,
    IndPoomsaeScores P,
    GenderTbl G,
    TTDivisionNames D,
    CategoryTbl C,
    TTRound R
WHERE
    E.DatabaseID = P.DatabaseID
    AND G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    AND D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    AND C.DatabaseID = E.DatabaseID AND P.Category = C.Category_ID
    AND R.DatabaseID = E.DatabaseID AND R.Round_ID = P.RoundName
    AND P.Acc_R_A <> -1
    AND E.EventName = :eventname