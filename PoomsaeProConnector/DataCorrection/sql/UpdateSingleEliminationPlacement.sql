UPDATE PoomsaeScores
SET Placement = POWER(2, (16 - RoundName) - 1) + 1
WHERE
    Acc_R_A <> -1 --Competition Happened
    AND RoundName BETWEEN 9 AND 14 --Single Elimination Round
	AND Placement = 0 --Athlete has no place in the round
	AND NOT EXISTS ( --Competitor not in next round
		SELECT 'X' FROM PoomsaeScores PE 
		WHERE 
			DatabaseID = PE.DatabaseID 
			AND Gender = PE.Gender 
			AND Division = PE.Division
			AND Category = PE.Category
			AND CompetitorNbr = PE.CompetitorNbr
			AND RoundName + 1 = PE.RoundName
	)