def Result_Write(F,Team1,Team1Score,Team2,Team2Score,BetType,BetTeam,BetLine,BetAmount,WinLose,BetNet):
	
	# Get get a new line
	F.write("\n")
	Statement1 = str(Team1) + "..." + str(Team1Score) + "..." + str(Team2) + "..." + str(Team2Score)
	F.write(Statement1)
	
	F.write("\n")

	Statement2 = str(BetType) + "..." + str(BetTeam) + "..." + str(BetLine) + "..." + str(BetAmount) + "..." + str(WinLose) + "..." + str(BetNet)	

	F.write(Statement2)
	
	F.write("\n")
	F.write("\n")
