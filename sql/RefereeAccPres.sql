--Poomsae A for non-Team Trials
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
	SE.MatchNo,
    REF.RefereeName,
    P.FormName_A as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_A
        WHEN 'J1' THEN P.Acc_J1_A
        WHEN 'J2' THEN P.Acc_J2_A
        WHEN 'J3' THEN P.Acc_J3_A
        WHEN 'J4' THEN P.Acc_J4_A
        WHEN 'J5' THEN P.Acc_J5_A
        WHEN 'J6' THEN P.Acc_J6_A
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_A
        WHEN 'J1' THEN P.Pre_J1_A
        WHEN 'J2' THEN P.Pre_J2_A
        WHEN 'J3' THEN P.Pre_J3_A
        WHEN 'J4' THEN P.Pre_J4_A
        WHEN 'J5' THEN P.Pre_J5_A
        WHEN 'J6' THEN P.Pre_J6_A
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_A as TotalAccuracy,
    P.Pre_Avg_A as TotalPresentation
FROM
    Events E,
    GenderTbl G,
    DivisionNames D,
    CategoryTbl C,
    RoundTbl RND,
    RefereeAssignment REF,
	PoomsaeScores P
	LEFT OUTER JOIN SEMatchList SE
		ON SE.Gender = P.Gender
			AND SE.Division = P.Division
			AND P.Category = SE.Category
			AND SE.Round = P.RoundName
			AND (SE.MatchRef = P.OrderOfPerform
				OR (SE.MatchRef = POWER(2,7-(P.RoundName)-9) + 1 - P.OrderOfPerform
					AND POWER(2,7-(P.RoundName)-9) + 1 - P.OrderOfPerform < P.OrderOfPerform
					)
				)
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
	AND (REF.MatchNumber <= 0
		OR (REF.MatchNumber > 0
			AND REF.MatchNumber = SE.MatchNo
			)
		)
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
	SE.MatchNo,
    REF.RefereeName,
    P.FormName_B as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_B
        WHEN 'J1' THEN P.Acc_J1_B
        WHEN 'J2' THEN P.Acc_J2_B
        WHEN 'J3' THEN P.Acc_J3_B
        WHEN 'J4' THEN P.Acc_J4_B
        WHEN 'J5' THEN P.Acc_J5_B
        WHEN 'J6' THEN P.Acc_J6_B
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_B
        WHEN 'J1' THEN P.Pre_J1_B
        WHEN 'J2' THEN P.Pre_J2_B
        WHEN 'J3' THEN P.Pre_J3_B
        WHEN 'J4' THEN P.Pre_J4_B
        WHEN 'J5' THEN P.Pre_J5_B
        WHEN 'J6' THEN P.Pre_J6_B
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_B as TotalAccuracy,
    P.Pre_Avg_B as TotalPresentation
FROM
    Events E,
    GenderTbl G,
    DivisionNames D,
    CategoryTbl C,
    RoundTbl RND,
    RefereeAssignment REF,
	PoomsaeScores P
	LEFT OUTER JOIN SEMatchList SE
		ON SE.Gender = P.Gender
			AND SE.Division = P.Division
			AND P.Category = SE.Category
			AND SE.Round = P.RoundName
			AND (SE.MatchRef = P.OrderOfPerform
				OR (SE.MatchRef = POWER(2,7-(P.RoundName)-9) + 1 - P.OrderOfPerform
					AND POWER(2,7-(P.RoundName)-9) + 1 - P.OrderOfPerform < P.OrderOfPerform
					)
				)
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
	AND (REF.MatchNumber <= 0
		OR (REF.MatchNumber > 0
			AND REF.MatchNumber = SE.MatchNo
			)
		)
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
	SE.MatchNo,
    REF.RefereeName,
    P.FormName_T as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_T
        WHEN 'J1' THEN P.Acc_J1_T
        WHEN 'J2' THEN P.Acc_J2_T
        WHEN 'J3' THEN P.Acc_J3_T
        WHEN 'J4' THEN P.Acc_J4_T
        WHEN 'J5' THEN P.Acc_J5_T
        WHEN 'J6' THEN P.Acc_J6_T
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_T
        WHEN 'J1' THEN P.Pre_J1_T
        WHEN 'J2' THEN P.Pre_J2_T
        WHEN 'J3' THEN P.Pre_J3_T
        WHEN 'J4' THEN P.Pre_J4_T
        WHEN 'J5' THEN P.Pre_J5_T
        WHEN 'J6' THEN P.Pre_J6_T
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_T as TotalAccuracy,
    P.Pre_Avg_T as TotalPresentation
FROM
    Events E,
    GenderTbl G,
    DivisionNames D,
    CategoryTbl C,
    RoundTbl RND,
    RefereeAssignment REF,
	PoomsaeScores P
	LEFT OUTER JOIN SEMatchList SE
		ON SE.DatabaseID = P.DatabaseID
			AND	SE.Gender = P.Gender
			AND SE.Division = P.Division
			AND P.Category = SE.Category
			AND SE.Round = P.RoundName
			AND ((SE.Round >= 9 --Single Elimination
				AND ( 
					P.OrderOfPerform = POWER(2,6-(P.RoundName-9)) + SE.MatchRef --1/2 of round 2^7=128
					OR P.OrderOfPerform = POWER(2,6-(P.RoundName-9)) + 1 - SE.MatchRef
					))
				OR SE.Round < 9 --CutOff
				)
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
	AND (REF.MatchNumber <= 0
		OR (REF.MatchNumber > 0
			AND REF.MatchNumber = SE.MatchNo
			)
		)
UNION
--Poomsae A for Team Trials Pre-2026
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    '',
    REF.RefereeName,
    P.FormName_A as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_A
        WHEN 'J1' THEN P.Acc_J1_A
        WHEN 'J2' THEN P.Acc_J2_A
        WHEN 'J3' THEN P.Acc_J3_A
        WHEN 'J4' THEN P.Acc_J4_A
        WHEN 'J5' THEN P.Acc_J5_A
        WHEN 'J6' THEN P.Acc_J6_A
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_A
        WHEN 'J1' THEN P.Pre_J1_A
        WHEN 'J2' THEN P.Pre_J2_A
        WHEN 'J3' THEN P.Pre_J3_A
        WHEN 'J4' THEN P.Pre_J4_A
        WHEN 'J5' THEN P.Pre_J5_A
        WHEN 'J6' THEN P.Pre_J6_A
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
    AND E.StartDate < '2026-01-01' --2026 Team Trials Change
UNION
--Poomsae T for Team Trials Pre-2026
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    '',
    REF.RefereeName,
    P.FormName_T as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_T
        WHEN 'J1' THEN P.Acc_J1_T
        WHEN 'J2' THEN P.Acc_J2_T
        WHEN 'J3' THEN P.Acc_J3_T
        WHEN 'J4' THEN P.Acc_J4_T
        WHEN 'J5' THEN P.Acc_J5_T
        WHEN 'J6' THEN P.Acc_J6_T
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_T
        WHEN 'J1' THEN P.Pre_J1_T
        WHEN 'J2' THEN P.Pre_J2_T
        WHEN 'J3' THEN P.Pre_J3_T
        WHEN 'J4' THEN P.Pre_J4_T
        WHEN 'J5' THEN P.Pre_J5_T
        WHEN 'J6' THEN P.Pre_J6_T
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
    AND E.StartDate < '2026-01-01' --2026 Team Trials Change
UNION
--Poomsae A for Team Trials Post 2026
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    '',
    REF.RefereeName,
    P.FormName_A as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_A
        WHEN 'J1' THEN P.Acc_J1_A
        WHEN 'J2' THEN P.Acc_J2_A
        WHEN 'J3' THEN P.Acc_J3_A
        WHEN 'J4' THEN P.Acc_J4_A
        WHEN 'J5' THEN P.Acc_J5_A
        WHEN 'J6' THEN P.Acc_J6_A
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_A
        WHEN 'J1' THEN P.Pre_J1_A
        WHEN 'J2' THEN P.Pre_J2_A
        WHEN 'J3' THEN P.Pre_J3_A
        WHEN 'J4' THEN P.Pre_J4_A
        WHEN 'J5' THEN P.Pre_J5_A
        WHEN 'J6' THEN P.Pre_J6_A
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_A as TotalAccuracy,
    P.Pre_Avg_A as TotalPresentation
FROM
    Events E,
    IndPoomsaeScores P,
    GenderTbl G,
    DivisionNames D, --Instead of TTDivisionNames
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
    AND E.StartDate >= '2026-01-01' --2026 Team Trials Change
UNION
--Poomsae T for Team Trials Post-2026
SELECT 
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    P.RingNbr,
    P.Performance_ID,
    '',
    REF.RefereeName,
    P.FormName_T as Poomsae,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_T
        WHEN 'J1' THEN P.Acc_J1_T
        WHEN 'J2' THEN P.Acc_J2_T
        WHEN 'J3' THEN P.Acc_J3_T
        WHEN 'J4' THEN P.Acc_J4_T
        WHEN 'J5' THEN P.Acc_J5_T
        WHEN 'J6' THEN P.Acc_J6_T
        ELSE NULL
    END) AS Accuracy,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_T
        WHEN 'J1' THEN P.Pre_J1_T
        WHEN 'J2' THEN P.Pre_J2_T
        WHEN 'J3' THEN P.Pre_J3_T
        WHEN 'J4' THEN P.Pre_J4_T
        WHEN 'J5' THEN P.Pre_J5_T
        WHEN 'J6' THEN P.Pre_J6_T
        ELSE NULL
    END) AS Presentation,
    P.Acc_Avg_T as TotalAccuracy,
    P.Pre_Avg_T as TotalPresentation
FROM
    Events E,
    IndPoomsaeScores P,
    GenderTbl G,
    DivisionNames D, --Instead of TTDivisionNames
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
    AND E.StartDate >= '2026-01-01' --2026 Team Trials Change