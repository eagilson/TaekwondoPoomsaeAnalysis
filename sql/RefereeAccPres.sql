--Poomsae A for non-Team Trials
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    REF.RefereeName,
    'Poomsae A' as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_A
        WHEN 'J1' THEN P.Acc_J1_A
        WHEN 'J2' THEN P.Acc_J1_A
        WHEN 'J3' THEN P.Acc_J1_A
        WHEN 'J4' THEN P.Acc_J1_A
        WHEN 'J5' THEN P.Acc_J1_A
        WHEN 'J6' THEN P.Acc_J1_A
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_A
        WHEN 'J1' THEN P.Pre_J1_A
        WHEN 'J2' THEN P.Pre_J1_A
        WHEN 'J3' THEN P.Pre_J1_A
        WHEN 'J4' THEN P.Pre_J1_A
        WHEN 'J5' THEN P.Pre_J1_A
        WHEN 'J6' THEN P.Pre_J1_A
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_A as TotalAccuracy,
    P.Pre_Avg_A as TotalPresentation
FROM
    Events E,
    PoomsaeScores P,
    GenderTbl G,
    DivisionNames D,
    CategoryTbl C,
    RoundTbl RND,
    RefereeAssignment REF
WHERE
    E.DatabaseID = P.DatabaseID
    AND G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    AND D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    AND C.DatabaseID = E.DatabaseID AND P.Category = C.Category_ID
    AND RND.DatabaseID = E.DatabaseID AND RND.Round_ID = P.RoundName
    AND REF.EventName = E.EventName AND REF.Division = D.Division 
    AND REF.Gender = G.Gender AND REF.Category = C.Category 
    AND REF.Round = RND.Round AND REF.RingNbr = P.RingNbr
    AND P.Acc_R_A <> -1
UNION
--Poomsae B for non-Team Trials
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    REF.RefereeName,
    'Poomsae B' as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_T
        WHEN 'J1' THEN P.Acc_J1_B
        WHEN 'J2' THEN P.Acc_J1_B
        WHEN 'J3' THEN P.Acc_J1_B
        WHEN 'J4' THEN P.Acc_J1_B
        WHEN 'J5' THEN P.Acc_J1_B
        WHEN 'J6' THEN P.Acc_J1_B
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_B
        WHEN 'J1' THEN P.Pre_J1_B
        WHEN 'J2' THEN P.Pre_J1_B
        WHEN 'J3' THEN P.Pre_J1_B
        WHEN 'J4' THEN P.Pre_J1_B
        WHEN 'J5' THEN P.Pre_J1_B
        WHEN 'J6' THEN P.Pre_J1_B
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_B as TotalAccuracy,
    P.Pre_Avg_B as TotalPresentation
FROM
    Events E,
    PoomsaeScores P,
    GenderTbl G,
    DivisionNames D,
    CategoryTbl C,
    RoundTbl RND,
    RefereeAssignment REF
WHERE
    E.DatabaseID = P.DatabaseID
    AND G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    AND D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    AND C.DatabaseID = E.DatabaseID AND P.Category = C.Category_ID
    AND RND.DatabaseID = E.DatabaseID AND RND.Round_ID = P.RoundName
    AND REF.EventName = E.EventName AND REF.Division = D.Division 
    AND REF.Gender = G.Gender AND REF.Category = C.Category 
    AND REF.Round = RND.Round AND REF.RingNbr = P.RingNbr
    AND P.Acc_R_B <> -1
UNION
--Poomsae T for non-Team Trials
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    REF.RefereeName,
    'Poomsae B' as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_T
        WHEN 'J1' THEN P.Acc_J1_T
        WHEN 'J2' THEN P.Acc_J1_T
        WHEN 'J3' THEN P.Acc_J1_T
        WHEN 'J4' THEN P.Acc_J1_T
        WHEN 'J5' THEN P.Acc_J1_T
        WHEN 'J6' THEN P.Acc_J1_T
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_T
        WHEN 'J1' THEN P.Pre_J1_T
        WHEN 'J2' THEN P.Pre_J1_T
        WHEN 'J3' THEN P.Pre_J1_T
        WHEN 'J4' THEN P.Pre_J1_T
        WHEN 'J5' THEN P.Pre_J1_T
        WHEN 'J6' THEN P.Pre_J1_T
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_T as TotalAccuracy,
    P.Pre_Avg_T as TotalPresentation
FROM
    Events E,
    PoomsaeScores P,
    GenderTbl G,
    DivisionNames D,
    CategoryTbl C,
    RoundTbl RND,
    RefereeAssignment REF
WHERE
    E.DatabaseID = P.DatabaseID
    AND G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    AND D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    AND C.DatabaseID = E.DatabaseID AND P.Category = C.Category_ID
    AND RND.DatabaseID = E.DatabaseID AND RND.Round_ID = P.RoundName
    AND REF.EventName = E.EventName AND REF.Division = D.Division 
    AND REF.Gender = G.Gender AND REF.Category = C.Category 
    AND REF.Round = RND.Round AND REF.RingNbr = P.RingNbr
    AND P.Acc_R_T <> -1
UNION
--Poomsae A for non-Team Trials
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    REF.RefereeName,
    'Poomsae A' as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_A
        WHEN 'J1' THEN P.Acc_J1_A
        WHEN 'J2' THEN P.Acc_J1_A
        WHEN 'J3' THEN P.Acc_J1_A
        WHEN 'J4' THEN P.Acc_J1_A
        WHEN 'J5' THEN P.Acc_J1_A
        WHEN 'J6' THEN P.Acc_J1_A
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_A
        WHEN 'J1' THEN P.Pre_J1_A
        WHEN 'J2' THEN P.Pre_J1_A
        WHEN 'J3' THEN P.Pre_J1_A
        WHEN 'J4' THEN P.Pre_J1_A
        WHEN 'J5' THEN P.Pre_J1_A
        WHEN 'J6' THEN P.Pre_J1_A
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_A as TotalAccuracy,
    P.Pre_Avg_A as TotalPresentation
FROM
    Events E,
    IndPoomsaeScores P,
    GenderTbl G,
    TTDivisionNames D,
    CategoryTbl C,
    TTRound RND,
    RefereeAssignment REF
WHERE
    E.DatabaseID = P.DatabaseID
    AND G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    AND D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    AND C.DatabaseID = E.DatabaseID AND P.Category = C.Category_ID
    AND RND.DatabaseID = E.DatabaseID AND RND.Round_ID = P.RoundName
    AND REF.EventName = E.EventName AND REF.Division = D.Division 
    AND REF.Gender = G.Gender AND REF.Category = C.Category 
    AND REF.Round = RND.Round AND REF.RingNbr = P.RingNbr
    AND P.Acc_R_A <> -1
UNION
--Poomsae T for non-Team Trials
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    REF.RefereeName,
    'Poomsae B' as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_T
        WHEN 'J1' THEN P.Acc_J1_T
        WHEN 'J2' THEN P.Acc_J1_T
        WHEN 'J3' THEN P.Acc_J1_T
        WHEN 'J4' THEN P.Acc_J1_T
        WHEN 'J5' THEN P.Acc_J1_T
        WHEN 'J6' THEN P.Acc_J1_T
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_T
        WHEN 'J1' THEN P.Pre_J1_T
        WHEN 'J2' THEN P.Pre_J1_T
        WHEN 'J3' THEN P.Pre_J1_T
        WHEN 'J4' THEN P.Pre_J1_T
        WHEN 'J5' THEN P.Pre_J1_T
        WHEN 'J6' THEN P.Pre_J1_T
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_T as TotalAccuracy,
    P.Pre_Avg_T as TotalPresentation
FROM
    Events E,
    IndPoomsaeScores P,
    GenderTbl G,
    TTDivisionNames D,
    CategoryTbl C,
    TTRound RND,
    RefereeAssignment REF
WHERE
    E.DatabaseID = P.DatabaseID
    AND G.DatabaseID = E.DatabaseID AND G.Gender_ID = P.Gender
    AND D.DatabaseID = E.DatabaseID AND D.Division_ID = P.Division
    AND C.DatabaseID = E.DatabaseID AND P.Category = C.Category_ID
    AND RND.DatabaseID = E.DatabaseID AND RND.Round_ID = P.RoundName
    AND REF.EventName = E.EventName AND REF.Division = D.Division 
    AND REF.Gender = G.Gender AND REF.Category = C.Category 
    AND REF.Round = RND.Round AND REF.RingNbr = P.RingNbr
    AND P.Acc_R_T <> -1