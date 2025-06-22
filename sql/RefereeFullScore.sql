--non-Team Trials
SELECT 
    'Standard' AS ScoreSource,
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    RND.Round_ID,
    P.RingNbr,
    P.Performance_ID,
	SE.MatchNo,
    P.OrderOfPerform,
    REF.RefereeName,
    P.FormName_A,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_A
        WHEN 'J1' THEN P.Acc_J1_A
        WHEN 'J2' THEN P.Acc_J2_A
        WHEN 'J3' THEN P.Acc_J3_A
        WHEN 'J4' THEN P.Acc_J4_A
        WHEN 'J5' THEN P.Acc_J5_A
        WHEN 'J6' THEN P.Acc_J6_A
        ELSE NULL
    END) AS Accuracy_A,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_A
        WHEN 'J1' THEN P.Pre_J1_A
        WHEN 'J2' THEN P.Pre_J2_A
        WHEN 'J3' THEN P.Pre_J3_A
        WHEN 'J4' THEN P.Pre_J4_A
        WHEN 'J5' THEN P.Pre_J5_A
        WHEN 'J6' THEN P.Pre_J6_A
        ELSE NULL
    END) AS Presentation_A,
    P.Acc_Avg_A,
    P.Pre_Avg_A,
    P.FormName_B,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_B
        WHEN 'J1' THEN P.Acc_J1_B
        WHEN 'J2' THEN P.Acc_J2_B
        WHEN 'J3' THEN P.Acc_J3_B
        WHEN 'J4' THEN P.Acc_J4_B
        WHEN 'J5' THEN P.Acc_J5_B
        WHEN 'J6' THEN P.Acc_J6_B
        ELSE NULL
    END) AS Accuracy_B,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_B
        WHEN 'J1' THEN P.Pre_J1_B
        WHEN 'J2' THEN P.Pre_J2_B
        WHEN 'J3' THEN P.Pre_J3_B
        WHEN 'J4' THEN P.Pre_J4_B
        WHEN 'J5' THEN P.Pre_J5_B
        WHEN 'J6' THEN P.Pre_J6_B
        ELSE NULL
    END) AS Presentation_B,
    P.Acc_Avg_B,
    P.Pre_Avg_B,
    P.FormName_T,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_T
        WHEN 'J1' THEN P.Acc_J1_T
        WHEN 'J2' THEN P.Acc_J2_T
        WHEN 'J3' THEN P.Acc_J3_T
        WHEN 'J4' THEN P.Acc_J4_T
        WHEN 'J5' THEN P.Acc_J5_T
        WHEN 'J6' THEN P.Acc_J6_T
        ELSE NULL
    END) AS Accuracy_T,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_T
        WHEN 'J1' THEN P.Pre_J1_T
        WHEN 'J2' THEN P.Pre_J2_T
        WHEN 'J3' THEN P.Pre_J3_T
        WHEN 'J4' THEN P.Pre_J4_T
        WHEN 'J5' THEN P.Pre_J5_T
        WHEN 'J6' THEN P.Pre_J6_T
        ELSE NULL
    END) AS Presentation_T,
    P.Acc_Avg_T,
    P.Pre_Avg_T,
    P.Form_Score_AB, 
	P.Presentation_Total, 
	P.Full_Score, 
	P.TieBreaker_Score, 
	P.TieBreaker_Total,
    P.Placement
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
--Team Trials
SELECT 
    'Team Trials' AS ScoreSource,
    E.EventName,
    D.Division,
    G.Gender,
    C.Category,
    RND.Round,
    RND.Round_ID,
    P.RingNbr,
    P.Performance_ID,
    '',
    P.OrderOfPerform,
    REF.RefereeName,
    P.FormName_A,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_A
        WHEN 'J1' THEN P.Acc_J1_A
        WHEN 'J2' THEN P.Acc_J2_A
        WHEN 'J3' THEN P.Acc_J3_A
        WHEN 'J4' THEN P.Acc_J4_A
        WHEN 'J5' THEN P.Acc_J5_A
        WHEN 'J6' THEN P.Acc_J6_A
        ELSE NULL
    END) AS Accuracy_A,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_A
        WHEN 'J1' THEN P.Pre_J1_A
        WHEN 'J2' THEN P.Pre_J2_A
        WHEN 'J3' THEN P.Pre_J3_A
        WHEN 'J4' THEN P.Pre_J4_A
        WHEN 'J5' THEN P.Pre_J5_A
        WHEN 'J6' THEN P.Pre_J6_A
        ELSE NULL
    END) AS Presentation_A,
    P.Acc_Avg_A,
    P.Pre_Avg_A,
    'None',
    -1 AS Accuracy_B,
    -1 AS Presentation_B,
    -1 AS Acc_Avg_B,
    -1 AS Pre_Avg_B,
    P.FormName_T,
    (CASE REF.Position
        WHEN 'R' THEN P.Acc_R_T
        WHEN 'J1' THEN P.Acc_J1_T
        WHEN 'J2' THEN P.Acc_J2_T
        WHEN 'J3' THEN P.Acc_J3_T
        WHEN 'J4' THEN P.Acc_J4_T
        WHEN 'J5' THEN P.Acc_J5_T
        WHEN 'J6' THEN P.Acc_J6_T
        ELSE NULL
    END) AS Accuracy_T,
    (CASE REF.Position
        WHEN 'R' THEN P.Pre_R_T
        WHEN 'J1' THEN P.Pre_J1_T
        WHEN 'J2' THEN P.Pre_J2_T
        WHEN 'J3' THEN P.Pre_J3_T
        WHEN 'J4' THEN P.Pre_J4_T
        WHEN 'J5' THEN P.Pre_J5_T
        WHEN 'J6' THEN P.Pre_J6_T
        ELSE NULL
    END) AS Presentation_T,
    P.Acc_Avg_T,
    P.Pre_Avg_T,
    P.Form_Score_AB, 
	P.Presentation_Total, 
	P.Full_Score, 
	P.TieBreaker_Score, 
	P.TieBreaker_Total,
    P.Placement
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