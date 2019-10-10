"""
This script reads the scores from the week's football games and compares those
scores with the betting sheets from the participants in the fantasy league.
It determines how each person's bets fared and prints personal bet result
text files and each participant.
"""

import pandas

# Result_Write is used to write the bet results to a text file
def Result_Write(F,Team1,Team1Score,Team2,Team2Score,BetType,BetTeam,BetLine,BetAmount,WinLose,BetNet):
    
    # Get get a new line
    F.write("\n")
    
    # First part of the statement is the scoreboard
    Statement1 = str(Team1) + "..." + str(Team1Score) + "..." + str(Team2) + "..." + str(Team2Score)
    F.write(Statement1)
    
    # Go to the next line
    F.write("\n")

    # Second part of the statement says what the bet was and what the result is
    Statement2 = str(BetType) + "..." + str(BetTeam) + "..." + str(BetLine) + "..." + str(BetAmount) + "..." + str(WinLose) + "..." + str(BetNet)    
    F.write(Statement2)

    # Two lines to make the text file look better
    F.write("\n\n")

# Define what week number you're looking at so that you can load in the data from the excel files
week_number = input("Week Number: ")

# Read in the file containing the scores using pandas
score_filename = 'CFB_Week' + str(week_number) + '_Scores.xls'

try:
    scoresheet_holder = pandas.ExcelFile(score_filename)
    scoresheet = scoresheet_holder.parse('Sheet1')
except:
    try:
        score_filename = 'CFB_Week' + str(week_number) + '_Scores.xlsx'
        scoresheet_holder = pandas.ExcelFile(score_filename)
        scoresheet = scoresheet_holder.parse('Sheet1')
    except:
        print("Score file not found!")

# Define the names of the participants.
#Names = ['AdamFoster', 'DustinFishelman', 'JeremyMuesing', 'ZachMcCusker', 'AaronMcCusker', 'ZachMaas', 'LukeWheeler']

Names = ['AaronMcCusker']

# Value will be an array where each item is the net money for each person with the first index corresponding to the first listed person in Names
Value = [0]

# n corresponds to which person you're looking at. N = Names[n]
n = 0

# Run through every person listed in Names
for N in Names:

    # Create the text file that will contain the results for the corresponding participant
    Text_Filename = 'CFB_Week' + str(week_number) + '_' + N + '_Results.txt'
    F = open(Text_Filename,"w")
    
    # Put a legend at the top of the text file
    F.write("Week {0} Results\n\n".format(week_number))
    F.write("Team 1 ... Team 1 Score ... Team 2 ... Team 2 Score ...\nBet Type ... Bet Team ... Bet Line ... Bet Amount ... Win or Lose ... Bet Net")
    F.write("\n\n")
    
    # If you aren't dealing with the first person, you need to append Value to accomodate a new participant
    if n > 0:
        Value.append(0)
    
    # Read in the bet file from the person N 
    # Since the file extensions can be different, try both before you toss an error
    for extensions in ['.xls','.xlsx']:
        bets_filename = 'CFB_Week' + str(week_number) + '_' + N + extensions
        try:
            bets_holder = pandas.ExcelFile(bets_filename)
            break
        except FileNotFoundError:
            continue
    else:
        FileNotFoundError()
        
    bets = bets_holder.parse('Sheet1')
    
    # In the scoresheet, run through every matchup
    for i in range(int(len(scoresheet.index)/2)):
        
        # Record the teams involved and the score from each team
        Team1 = scoresheet.loc[i*2]['Matchup']
        Team1Score = scoresheet.loc[i*2]['Score']
        Team2 = scoresheet.loc[i*2 + 1]['Matchup']
        Team2Score = scoresheet.loc[i*2 + 1]['Score']
        
        # In the event that a game did not occur, you must MANUALLY enter "NO GAME" into the score column for the teams that did not play
        # Games that did not occur are given a push (ie 0 net money)
        # Still write to text file so that there's traceability for what happened to the bet on the game that did not occur
        if Team1Score == "NO GAME" or Team2Score == "NO GAME":
            if float(bets.loc[i*2]['Bet']) > 0 or float(bets.loc[i*2 + 1]['Bet']) > 0:
               Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Moneyline","Game did not occur","N/A","N/A","Push",'0')
            if float(bets.loc[i*2]['Bet.1']) > 0 or float(bets.loc[i*2 + 1]['Bet.1']) > 0:
                Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread","Game did not occur","N/A","N/A","Push",'0')
            if float(bets.loc[i*2]['Bet.2']) > 0 or float(bets.loc[i*2 + 1]['Bet.2']) > 0:
                Result_Write(F,Team1,Team1Score,Team2,Team2Score,"O/U","Game did not occur","N/A","N/A","Push",'0')
            continue

        # Check if the person whose excel file you're reading bet on the matchup that you're looking at. This statement checks if the person bet Money Line on the matchup
        if float(bets.loc[i*2]['Bet']) > 0 or float(bets.loc[i*2 + 1]['Bet']) > 0:
            
            # If they did bet the Money Line on this matchup, figure out which team they bet on. Don't use an if/else staement here just in case someone decided to idiotically bet moneyline on both teams in a single matchup
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
                        # Holy moly there was a tie in a college football game!!
                        # Player gets a push
                        Value[n] = Value[n]
                        Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team1,bets.loc[i*2]['Money Line'],bets.loc[i*2]['Bet'],"Push",str(0))
                    
                    # If none of these things happen, something definitely went wrong
                    else:
                        Statement = "Something went wrong with the score definition for " + N
                        print(Statement)

                # The moneyline being negative indicates that the person bet on the favorite
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
                        # Holy holy there was a tie in a college football game
                        # Player gets a push
                        Value[n] = Value[n]
                        
                        # Write to text file
                        Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Money Line",Team1,bets.loc[i*2]['Money Line'],bets.loc[i*2]['Bet'],"Push",str(0))

                    else:
                        Statement = "Something went wrong with the score definition on the moneyline for " + N
                        print(Statement)

                # If no cases occur, something went wrong                        
                else:
                    Statement = 'Something went wrong with the Money Line bet for' + N
                    print(Statement)
                
            # If this is true, the participant bet moneyline on the second team lister in scorecard
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
                        # Holy moly there was a tie in a college football game
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
                        # Holy moly there was a tie in a college football game
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
                    Spread = float(bets.loc[i*2 + 1]['Spread'])
                    Favorite_Score = int(scoresheet.loc[i*2 + 1]['Score'])
                    Favorite_Adjusted_Score = Favorite_Score + Spread
                    Underdog_Score = int(scoresheet.loc[i*2]['Score'])

                    # Person loses bet
                    if Favorite_Adjusted_Score > Underdog_Score:

                        Net = -float(bets.loc[i*2]['Bet.1'])
                        Value[n] = Value[n] + Net

                        # Write to the text file
                        Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,"+" + str(-1*float(bets.loc[i*2 + 1]['Spread'])),bets.loc[i*2]['Bet.1'],"Lose",Net)

                    # Person wins bet
                    elif Favorite_Adjusted_Score < Underdog_Score:
                        
                        Net = float(bets.loc[i*2]['Bet.1'])
                        Value[n] = Value[n] + Net
                        
                        # Write to the text file
                        Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,"+" + str(-1*float(bets.loc[i*2 + 1]['Spread'])),bets.loc[i*2]['Bet.1'],"Win",Net)

                    elif Favorite_Adjusted_Score == Underdog_Score:
                        # Push
                        Value[n] = Value[n]

                        # Write to the text file
                        Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team1,"+" + str(-1*float(bets.loc[i*2 + 1]['Spread'])),bets.loc[i*2]['Bet.1'],"Push",0)
                    
                    else:
                        Statement = 'An error occured with the spread bet for ' + N
                        print(Statement)
                
                # If the person bet the spread and did NOT bet on the underdog, then they bet on the favorite to cover
                else:
                    Spread = float(bets.loc[i*2]['Spread'])
                    Favorite_Score = int(scoresheet.loc[i*2]['Score'])
                    Favorite_Adjusted_Score = Favorite_Score + float(Spread)
                    Underdog_Score = int(scoresheet.loc[i*2 + 1]['Score'])

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

            # The person bet the spread on the second team in the matchup
            if float(bets.loc[i*2 + 1]['Bet.1']) > 0:

                # The person bet on the underdog in this matchup
                if bets.loc[i*2 + 1]['Spread'] == '-':
                    
                    # Determine the spread
                    Spread = float(bets.loc[i*2]['Spread'])

                    # Adjust the score for the favorite to reflect the spread handicap
                    Favorite_Score = int(scoresheet.loc[i*2]['Score'])
                    Favorite_Adjusted_Score = Favorite_Score + Spread
                    Underdog_Score = int(scoresheet.loc[i*2 + 1]['Score'])

                    # Person loses bet
                    if Favorite_Adjusted_Score > Underdog_Score:

                        Net = -float(bets.loc[i*2 + 1]['Bet.1'])
                        Value[n] = Value[n] + Net

                        # Write to text file
                        Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,"+" + str(-1*float(bets.loc[i*2]['Spread'])),bets.loc[i*2 + 1]['Bet.1'],"Lose",Net)

                    # Person wins bet
                    elif Favorite_Adjusted_Score < Underdog_Score:

                        Net = float(bets.loc[i*2 + 1]['Bet.1'])
                        Value[n] = Value[n] + Net

                        # Write to text file
                        Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,"+" + str(-1*float(bets.loc[i*2]['Spread'])),bets.loc[i*2 + 1]['Bet.1'],"Win",Net)
                    
                    # Push
                    elif Favorite_Adjusted_Score == Underdog_Score:
                        Value[n] = Value[n]

                        Result_Write(F,Team1,Team1Score,Team2,Team2Score,"Spread",Team2,"+" + str(-1*float(bets.loc[i*2]['Spread'])),bets.loc[i*2 + 1]['Bet.1'],"Push",0)

                    else:
                        Statement = 'An error occured with the spread bet for ' + N
                        print(Statement)

                # If the person bet the spread and did NOT bet on the underdog, then they bet on the favorite to cover
                else:
                    Spread = float(bets.loc[i*2 + 1]['Spread'])
                    Favorite_Score = int(scoresheet.loc[i*2 + 1]['Score'])
                    Favorite_Adjusted_Score = Favorite_Score + float(Spread)
                    Underdog_Score = int(scoresheet.loc[i*2]['Score'])

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

            # Gamescore is the sum total of the two teams' scores
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
             
    # Print results to the terminal so you can laugh at everyone's losses
    print('%(Name)s has a final value of %(Net).2f\n' % {'Name': N, 'Net': Value[n]})
    
    # Close the text file you've been writing to
    F.close()

    # This needs to be the last item in the entire for-loop. It indexes n to the next value so that your Value list is correct       
    n += 1




