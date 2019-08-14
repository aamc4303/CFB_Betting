# CFB_Betting

My friends and I always talked about how much money we'd make if we bet on college football games. We're not naive enough to think that we could actually win real money, but I wanted to see how we'd really do so I wrote up some code to determine who is really the best at betting on college football.

The first thing to do is to run vegas_insider_team_grabber.py which will pull the matchups, moneylines, spreads, and point totals from vegasinsider.com

Next, send the automatically created excel file to your friends, who will fill out the form and return it to you with their picks. They must bet exactly $10,000 per week (in fake money!!) for this league.

After the week concludes, run score_grabber.py which finds the scores for all of the matchups for the week. These are put into an Excel file as well.

Finally, run result_writer.py to compare your friends' bets with the scores from the week, and write the results to .txt files so everyone can see how they did.

Manually update the Scorecard.xls file each week with everyone's results. This will soon also be automated but I'm not there yet.
