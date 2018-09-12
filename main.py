import pandas
from Results_Writer import Result_Write

# Define what week number you're looking at so that you can load in the data from the excel files
week_number = input("Week Number: ")

# Read in the file containing the scores
score_filename = 'CFB_Week' + str(week_number) + '_Scores.xlsx'

scoresheet_holder = pandas.ExcelFile(score_filename)

scoresheet = scoresheet_holder.parse('Sheet1')

Names = ['AdamFoster', 'DustinFishelman', 'JeremyMuesing', 'ZachMcCusker', 'AaronMcCusker', 'ZacharyMaas', 'LukeWheeler']

# Value will be an array where each item is the net money for each person with the first index corresponding to the first listed person in Names
Value = [0]

# n corresponds to which person you're looking at. N = Names[n]
n = 0

for N in Names:

	Text_Filename = 'CFB_Week' + str(week_number) + '_' + N + '_Results.txt'
	F = open(Text_Filename,"w")
	F.write("Week {0} Results\n\n".format(week_number))
	F.write("Team 1 ... Team 1 Score ... Team 2 ... Team 2 Score ...\nBet Type ... Bet Team ... Bet Line ... Bet Amount ... Win or Lose ... Bet Net")

	F.write("\n")
	F.write("\n")
	
	if n > 0:
		Value.append(0)
	
	# Read in the bet file from the person N	
	bets_filename = 'CFB_Week' + str(week_number) + '_' + N + '.xlsx'
	bets_holder = pandas.ExcelFile(bets_filename)
	bets = bets_holder.parse('Sheet1')
	
	for i in range(int(len(scoresheet.index)/2)):
		
		Team1 = scoresheet.loc[i*2]['Matchup']
		Team1Score = scoresheet.loc[i*2]['Score']
		Team2 = scoresheet.loc[i*2 + 1]['Matchup']
		Team2Score = scoresheet.loc[i*2 + 1]['Score']

		# Check if the person whose excel file you're reading bet on the matchup that you're looking at. This statement checks if the person bet Money Line on the matchup
		if float(bets.loc[i*2]['Bet']) > 0 or float(bets.loc[i*2 + 1]['Bet']) > 0:
			
			# If they did bet the Money Line on this matchup, figure out which team they bet on. Don't use an if/else staement here just in case someone decided to idiotically bet Money Line on both teams

			if float(bets.loc[i*2]['Bet']) > 0:
					
				# Get the moneyline from the excel file				
				MoneyLine = int(bets.loc[i*2]['Money Line'])

				# Check to see if the person bet on the favorite or the underdog
				if MoneyLine > 0:
					# Player bet on the underdog

					# Check to see who won the matchup
					if Team1Score > Team2Score:
						# Player wins
						Net = (float(bets.loc[i*2]['Money Line'])/100)*float(bets.loc[i*2]['Bet'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team1,bets.loc[i*2]['Money Line'],bets.loc[i*2]['Bet'],"Win",str(Net))

					elif Team1Score < Team2Score:
						# Player loses
						Net = -float(bets.loc[i*2]['Bet'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team1,bets.loc[i*2]['Money Line'],bets.loc[i*2]['Bet'],"Lose",str(Net))


					elif Team1Score == Team2Score:
						# Holy shit there was a tie in a college football game
						# Player gets a push
						Value[n] = Value[n]
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team1,bets.loc[i*2]['Money Line'],bets.loc[i*2]['Bet'],"Push",str(0))
						
					else:
						Statement = "Something went wrong with the score definition for " + N
						print(Statement)

				elif MoneyLine < 0:
					# Player bet on the favorite

					# Check to see who won the matchup
					if Team1Score > Team2Score:
                                                # Player wins
						Net = (100/abs(float(bets.loc[i*2]['Money Line'])))*float(bets.loc[i*2]['Bet'])
						Value[n] = Value[n] + Net
						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team1,bets.loc[i*2]['Money Line'],bets.loc[i*2]['Bet'],"Win",Net)						

					elif Team1Score < Team2Score:
                                                # Player loses
						Net = -float(bets.loc[i*2]['Bet'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team1,bets.loc[i*2]['Money Line'],bets.loc[i*2]['Bet'],"Lose",Net)						
					elif Team1Score == Team2Score:
                                                # Holy shit there was a tie in a college football game
                                                # Player gets a push
						Value[n] = Value[n]
						
						# Write to text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team1,bets.loc[i*2]['Money Line'],bets.loc[i*2]['Bet'],"Push",str(0))

					else:
						Statement = "Something went wrong with the score definition on the moneyline for " + N
						print(Statement)
						
				else:
					print(Team1Score)
					print(Team2Score)
					print(MoneyLine)
					Statement = 'Something went wrong with the Money Line bet for' + N
					print(Statement)
				
			if float(bets.loc[i*2 + 1]['Bet']) > 0:

				# Get the moneyline from the excel file                         
				MoneyLine = int(bets.loc[i*2 + 1]['Money Line'])

                                # Check to see if the person bet on the favorite or the underdog
				if MoneyLine > 0:
                                        # Player bet on the underdog

                                        # Check to see who won the matchup
					if Team2Score > Team1Score:
                                                # Player wins
						Net = (float(bets.loc[i*2 + 1]['Money Line'])/100)*float(bets.loc[i*2 + 1]['Bet'])
						Value[n] = Value[n] + Net

						# Write to text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team2,bets.loc[i*2 + 1]['Money Line'],bets.loc[i*2 + 1]['Bet'],"Win",Net)

					elif Team2Score < Team1Score:
                                                # Player loses
						Net = -float(bets.loc[i*2 + 1]['Bet'])
						Value[n] = Value[n] + Net

						# Write to text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team2,bets.loc[i*2 + 1]['Money Line'],bets.loc[i*2 + 1]['Bet'],"Lose",Net)
						
					elif Team2Score == Team1Score:
                                                # Holy shit there was a tie in a college football game
                                                # Player gets a push
						Value[n] = Value[n]

						# Write to text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team2,bets.loc[i*2 + 1]['Money Line'],bets.loc[i*2 + 1]['Bet'],"Push",0)


				elif MoneyLine < 0:
                                        # Player bet on the favorite

                                        # Check to see who won the matchup
					if Team2Score > Team1Score:
                                                # Player wins
						Net = (100/abs(float(bets.loc[i*2 + 1]['Money Line'])))*float(bets.loc[i*2 + 1]['Bet'])
						Value[n] = Value[n] + Net
                                        
						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team2,bets.loc[i*2 + 1]['Money Line'],bets.loc[i*2 + 1]['Bet'],"Win",Net)

					elif Team2Score < Team1Score:
                                                # Player loses
						Net = -float(bets.loc[i*2 + 1]['Bet'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team2,bets.loc[i*2 + 1]['Money Line'],bets.loc[i*2 + 1]['Bet'],"Lose",Net)

					elif Team2Score == Team1Score:
                                                # Holy shit there was a tie in a college football game
                                                # Player gets a push
						Value[n] = Value[n]

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team2,bets.loc[i*2 + 1]['Money Line'],bets.loc[i*2 + 1]['Bet'],"Push",0)

		# Check if the person bet the spread
		if float(bets.loc[i*2]['Bet.1']) > 0 or float(bets.loc[i*2 + 1]['Bet.1']) > 0:
			
			if float(bets.loc[i*2]['Bet.1']) > 0:
				# Person bet on Team1				

				# Check if the person bet on the underdog or the favorite. This case corresponds to betting on the underdog. Person wins bet if the score of the team they bet on beats the other team when subtracting the spread from the favorite's score
				if bets.loc[i*2]['Spread'] == '-':
					Spread = bets.loc[i*2 + 1]['Spread']
					Favorite_Score = scoresheet.loc[i*2 + 1]['Score']
					Favorite_Adjusted_Score = Favorite_Score + Spread
					Underdog_Score = scoresheet.loc[i*2]['Score']

					# Person loses bet
					if Favorite_Adjusted_Score > Underdog_Score:

						Net = -float(bets.loc[i*2]['Bet.1'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,"+" + str(-1*bets.loc[i*2 + 1]['Spread']),bets.loc[i*2]['Bet.1'],"Lose",Net)

					# Person wins bet
					elif Favorite_Adjusted_Score < Underdog_Score:
						
						Net = float(bets.loc[i*2]['Bet.1'])
						Value[n] = Value[n] + Net
						
						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,"+" + str(-1*bets.loc[i*2 + 1]['Spread']),bets.loc[i*2]['Bet.1'],"Win",Net)

					elif Favorite_Adjusted_Score == Underdog_Score:
						# Push
						Value[n] = Value[n]

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,"+" + str(-1*bets.loc[i*2 + 1]['Spread']),bets.loc[i*2]['Bet.1'],"Push",0)
					
					else:
						Statement = 'An error occured with the spread bet for ' + N
						print(Statement)
				
				# If the person bet the spread and did NOT bet on the underdog, then they bet on the favorite to cover
				else:
					Spread = bets.loc[i*2]['Spread']
					Favorite_Score = scoresheet.loc[i*2]['Score']
					Favorite_Adjusted_Score = Favorite_Score + Spread
					Underdog_Score = scoresheet.loc[i*2 + 1]['Score']

					# Person wins bet
					if Favorite_Adjusted_Score > Underdog_Score:
						
						Net = float(bets.loc[i*2]['Bet.1'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,bets.loc[i*2]['Spread'],bets.loc[i*2]['Bet.1'],"Win",Net)

					# Person loses bet
					elif Favorite_Adjusted_Score < Underdog_Score:

						Net = -float(bets.loc[i*2]['Bet.1'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,bets.loc[i*2]['Spread'],bets.loc[i*2]['Bet.1'],"Lose",Net)

					# Push
					elif Favorite_Adjusted_Score == Underdog_Score:
						Value[n] = Value[n]

						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,bets.loc[i*2]['Spread'],bets.loc[i*2]['Bet.1'],"Push",0)
					# Else something went wrong
					else:
						Statement = 'An error occured with the spread bet for ' + N
						print(Statement)

			# The person bet on the second team in the matchup
			if float(bets.loc[i*2 + 1]['Bet.1']) > 0:

				# The person bet on the underdog in this matchup
				if bets.loc[i*2 + 1]['Spread'] == '-':
					Spread = bets.loc[i*2]['Spread']
					Favorite_Score = scoresheet.loc[i*2]['Score']
					Favorite_Adjusted_Score = Favorite_Score + Spread
					Underdog_Score = scoresheet.loc[i*2 + 1]['Score']

                                        # Person loses bet
					if Favorite_Adjusted_Score > Underdog_Score:

						Net = -float(bets.loc[i*2 + 1]['Bet.1'])
						Value[n] = Value[n] + Net

						# Write to text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,"+" + str(-1*bets.loc[i*2]['Spread']),bets.loc[i*2 + 1]['Bet.1'],"Lose",Net)

                                        # Person wins bet
					elif Favorite_Adjusted_Score < Underdog_Score:

						Net = float(bets.loc[i*2 + 1]['Bet.1'])
						Value[n] = Value[n] + Net

						# Write to text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,"+" + str(-1*bets.loc[i*2]['Spread']),bets.loc[i*2 + 1]['Bet.1'],"Win",Net)
					
					# Push
					elif Favorite_Adjusted_Score == Underdog_Score:
						Value[n] = Value[n]

						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,"+" + str(-1*bets.loc[i*2]['Spread']),bets.loc[i*2 + 1]['Bet.1'],"Push",0)

					else:
						Statement = 'An error occured with the spread bet for ' + N
						print(Statement)

				# If the person bet the spread and did NOT bet on the underdog, then they bet on the favorite to cover
				else:
					Spread = bets.loc[i*2 + 1]['Spread']
					Favorite_Score = scoresheet.loc[i*2 + 1]['Score']
					Favorite_Adjusted_Score = Favorite_Score + Spread
					Underdog_Score = scoresheet.loc[i*2]['Score']

                                        # Person wins bet
					if Favorite_Adjusted_Score > Underdog_Score:

						Net = float(bets.loc[i*2 + 1]['Bet.1'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,bets.loc[i*2 + 1]['Spread'],bets.loc[i*2 + 1]['Bet.1'],"Win",Net)

                                        # Person loses bet
					elif Favorite_Adjusted_Score < Underdog_Score:

						Net = -float(bets.loc[i*2 + 1]['Bet.1'])
						Value[n] = Value[n] + Net

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,bets.loc[i*2 + 1]['Spread'],bets.loc[i*2 + 1]['Bet.1'],"Lose",Net)

                                        # Push
					elif Favorite_Adjusted_Score == Underdog_Score:

						Value[n] = Value[n]

						# Write to the text file
						Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,bets.loc[i*2 + 1]['Spread'],bets.loc[i*2 + 1]['Bet.1'],"Push",0)

                                        # Else something went wrong
					else:
						Statement = 'An error occured with the spread bet for ' + N
						print(Statement)

		# Check to see if the person bet the Over/Under
		if float(bets.loc[i*2]['Bet.2']) > 0 or float(bets.loc[i*2 + 1]['Bet.2']) > 0:

			Gamescore = float(scoresheet.loc[i*2]['Score']) + float(scoresheet.loc[i*2 + 1]['Score'])

			# The person bet the over
			if float(bets.loc[i*2]['Bet.2']) > 0 and bets.loc[i*2]['O/U'] != '-':

				# The over is posted on the first team in the matchup
				if Gamescore > float(bets.loc[i*2]['O/U']):
					# Player won
					Net = float(bets.loc[i*2]['Bet.2'])
					Value[n] = Value[n] + Net

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Over","No Team",bets.loc[i*2]['O/U'],bets.loc[i*2]['Bet.2'],"Win",Net)

				elif Gamescore < float(bets.loc[i*2]['O/U']):
					# Player lost
					Net = -float(bets.loc[i*2]['Bet.2'])
					Value[n] = Value[n] + Net

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Over","No Team",bets.loc[i*2]['O/U'],bets.loc[i*2]['Bet.2'],"Lose",Net)

				elif Gamescore == float(bets.loc[i*2]['O/U']):
					# Push
					Value[n] = Value[n]
					
					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Over","No Team",bets.loc[i*2]['O/U'],bets.loc[i*2]['Bet.2'],"Push",0)

				else:
					# Something went wrong
					print('Something went wrong characterizing the O/U bet')

			# The person bet the over
			elif float(bets.loc[i*2 + 1]['Bet.2']) > 0 and bets.loc[i*2 + 1]['O/U'] != '-':

				# The over is posted on the second team in the matchup
				if Gamescore > float(bets.loc[i*2 + 1]['O/U']):
                                        # Player won
					Net = float(bets.loc[i*2 + 1]['Bet.2'])
					Value[n] = Value[n] + Net

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Over","No Team",bets.loc[i*2 + 1]['O/U'],bets.loc[i*2 + 1]['Bet.2'],"Win",Net)

				elif Gamescore < float(bets.loc[i*2 + 1]['O/U']):
                                        # Player lost
					Net = -float(bets.loc[i*2 + 1]['Bet.2'])
					Value[n] = Value[n] + Net

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Over","No Team",bets.loc[i*2 + 1]['O/U'],bets.loc[i*2 + 1]['Bet.2'],"Lose",Net)

				elif Gamescore == float(bets.loc[i*2 + 1]['O/U']):
                                        # Push
					Value[n] = Value[n]

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Over","No Team",bets.loc[i*2 + 1]['O/U'],bets.loc[i*2 + 1]['Bet.2'],"Push",0)

				else:
                                        # Something went wrong
                                        print('Something went wrong characterizing the O/U bet')


			# The person bet the under
			elif float(bets.loc[i*2]['Bet.2']) > 0 and bets.loc[i*2]['O/U'] == '-':

				if Gamescore < float(bets.loc[i*2 + 1]['O/U']):
					# Player wins
					Net = float(bets.loc[i*2]['Bet.2'])
					Value[n] = Value[n] + Net

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Under","No Team",bets.loc[i*2 + 1]['O/U'],bets.loc[i*2]['Bet.2'],"Win",Net)

				elif Gamescore > float(bets.loc[i*2 + 1]['O/U']):
					# Player loses
					Net = -float(bets.loc[i*2]['Bet.2'])
					Value[n] = Value[n] + Net

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Under","No Team",bets.loc[i*2 + 1]['O/U'],bets.loc[i*2]['Bet.2'],"Lose",Net)

				elif Gamescore == float(bets.loc[i*2 + 1]['O/U']):
					# Push
					Value[n] = Value[n]

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Under","No Team",bets.loc[i*2 + 1]['O/U'],bets.loc[i*2]['Bet.2'],"Push",0)

				else:
					# Something went wrong
					print('Something went wrong characterizing the O/U bet')

			# Player bet the under
			elif float(bets.loc[i*2 + 1]['Bet.2']) > 0 and bets.loc[i*2 + 1]['O/U'] == '-':
	
				if Gamescore < float(bets.loc[i*2]['O/U']):
					# Player wins
					Net = float(bets.loc[i*2 + 1]['Bet.2'])
					Value[n] = Value[n] + Net

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Under","No Team",bets.loc[i*2]['O/U'],bets.loc[i*2 + 1]['Bet.2'],"Win",Net)

				elif Gamescore > float(bets.loc[i*2]['O/U']):
					# Player loses
					Net = -float(bets.loc[i*2 + 1]['Bet.2'])
					Value[n] = Value[n] + Net

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Under","No Team",bets.loc[i*2]['O/U'],bets.loc[i*2 + 1]['Bet.2'],"Lose",Net)

				elif Gamescore == float(bets.loc[i*2]['O/U']):
					# Push
					Value[n] = Value[n]

					Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Under","No Team",bets.loc[i*2]['O/U'],bets.loc[i*2 + 1]['Bet.2'],"Push",0)

				else:
					# Something went wrong
					print('Something went wrong chracterizing the O/U bet')

			else:
				# The person somehow put the bet in the wrong spot
				Statement = N + ' put their O/U in the wrong spot'
				print(Statement)
				
			
	Statement = N + ' has a final value of ' + str(Value[n])
	print('%(Name)s has a final value of %(Net).2f\n' % {'Name': N, 'Net': Value[n]})
	
	# Write something at the end of the text file showing the final net
	F.write("\n\n")

	FinalStatement = 'Final Net Money for the week: $' + str(Value[n])

	F.write("\n")
	F.write(FinalStatement)
	# Close the text file you've been writing to
	F.close()

	# This needs to be the last item in the entire for-loop. It indexes n to the next value			
	n = n + 1




