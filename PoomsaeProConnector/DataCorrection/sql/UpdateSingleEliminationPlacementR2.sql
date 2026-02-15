UPDATE PoomsaeScores
SET Placement = 
	(SELECT PE.Placement FROM PoomsaeScores PE 
		WHERE 
			DatabaseID = PE.DatabaseID 
			AND Gender = PE.Gender 
			AND Division = PE.Division
			AND Category = PE.Category
			AND CompetitorNbr = PE.CompetitorNbr
			AND PE.RoundName = 16 --Placement Round
	)
WHERE
    Acc_R_A <> -1 --Competition Happened
    AND RoundName = 15 --Final Round
	AND Placement = 0 --Athlete has no place in the round