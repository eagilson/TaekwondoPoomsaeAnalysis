SELECT DISTINCT
    D.Division,
    G.Gender,
    C.Category,
    R.Round,
    E.CompDay, --Added for 2025 Nationals
    P.RingNbr,
    S.MatchNo --Modified for V3c
FROM 
    Events E
    INNER JOIN PoomsaeScores P
        ON E.DatabaseID = P.DatabaseID
    INNER JOIN GenderTbl G
        ON G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    INNER JOIN DivisionNames D
        ON D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    INNER JOIN CategoryTbl C
        ON C.DatabaseID = E.DatabaseID AND C.Category_ID = P.Category
    INNER JOIN RoundTbl R
        ON R.DatabaseID = E.DatabaseID AND R.Round_ID = P.RoundName
    LEFT OUTER JOIN SEMatchList S --Modified for V3c
        ON S.DatabaseID = E.DatabaseID
        AND S.Gender = P.Gender
        AND S.Division = P.Division
        AND S.Category = P.Category
        AND S.Round = P.RoundName
        --AND S.Complete = TRUE
        --Missing Ring Number join which causes duplication
WHERE
    P.Acc_R_A <> -1
    AND E.EventName = :eventname
--Team Trials
UNION
SELECT DISTINCT
    D.Division,
    G.Gender,
    C.Category,
    R.Round,
    E.CompDay, --Added for 2025 Nationals
    P.RingNbr,
    S.MatchNo --Modified for V3c
FROM 
    Events E
    INNER JOIN IndPoomsaeScores P
        ON E.DatabaseID = P.DatabaseID
    INNER JOIN GenderTbl G
        ON G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    INNER JOIN TTDivisionNames D
        ON D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    INNER JOIN CategoryTbl C
        ON C.DatabaseID = E.DatabaseID AND C.Category_ID = P.Category
    INNER JOIN TTRound R
        ON R.DatabaseID = E.DatabaseID AND R.Round_ID = P.RoundName
    LEFT OUTER JOIN SEMatchList S --Modified for V3c
        ON S.DatabaseID = E.DatabaseID
        AND S.Gender = P.Gender
        AND S.Division = P.Division
        AND S.Category = P.Category
        AND S.Round = P.RoundName
        --AND S.Complete = TRUE
WHERE
    P.Acc_R_A <> -1
    AND E.EventName = :eventname