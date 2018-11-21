"""
This script goes online and pulls the weekly scores from the internet and saves
those scores to an Excel file. The resulting Excel file is used in main.py to
determine how everyone's bets fared.
"""

from bs4 import BeautifulSoup
import requests
import xlsxwriter
import pandas

# Input week number
Week = input("Week Number: ")

# Establish your two file names. The blank file is the file without the bets but with the matchups included
ScoreFilename = "CFB_Week" + str(Week) + "_Scores.xlsx"
BlankFilename = "CFB_Week" + str(Week) + "_FirstnameLastname.xls"

# Create your scores excel file for the week
ScoreWorkbook = xlsxwriter.Workbook(ScoreFilename)
ScoreWorksheet = ScoreWorkbook.add_worksheet()
Excel_row = 0

# Write the headers to the score file
ScoreWorksheet.write(0,0,"Matchup")
ScoreWorksheet.write(0,1,"Score")

# The blank holder contains a blank betting sheet. This is important because it contains all of the matchups that participants were able to bet on
blank_holder = pandas.ExcelFile(BlankFilename)
blanksheet = blank_holder.parse('Sheet1')

# For every matchup in the blank betting sheet....
for i in range(int(len(blanksheet)/2)):
    
    # Increment the Excel row and determine the two team names in the matchup
	Excel_row = i*2
	Team1 = blanksheet.loc[i*2]['Matchup']
	Team2 = blanksheet.loc[i*2 + 1]['Matchup']

    # Write the team names to the new Excel file
	ScoreWorksheet.write(Excel_row + 1,0,Team1)
	ScoreWorksheet.write(Excel_row + 2,0,Team2)

# Get the scores page using requests and BS4
scores_page = requests.get('https://www.sports-reference.com/cfb/boxscores/')
scores_soup = BeautifulSoup(scores_page.text, 'html.parser')

# Pull all of the team names from the scores page
matchup_tables = scores_soup.find_all('table', {'class':"teams"})

# Go through all of the teams on the scores page. This page should include every matchup that participants were able to bet on
for i in range(len(matchup_tables)):
    
	# Grab the matchup and score from the html file
	matchup = matchup_tables[i].select("a")
	score = matchup_tables[i].find_all(class_="right")
	
	for j in range(int(len(blanksheet)/2)):
        
        # You only need ONE of the TWO team names from the blank bet sheet to match a team name in the score sheet in order to save it as the score
		if blanksheet.loc[j*2]['Matchup'] == matchup[0].text or blanksheet.loc[j*2+1]['Matchup'] == matchup[2].text:
			ScoreWorksheet.write(j*2 + 1,1,score[0].text)
			ScoreWorksheet.write(j*2 + 2,1,score[2].text)
		elif blanksheet.loc[j*2 + 1]['Matchup'] == matchup[0].text or blanksheet.loc[j*2]['Matchup'] == matchup[2].text:
			ScoreWorksheet.write(j*2 + 1,1,score[2].text)
			ScoreWorksheet.write(j*2 + 2,1,score[0].text)

# You're done writing scores so close the sheet
ScoreWorkbook.close()

# Read the newly populated scoresheet with pandas to check your work
PopulatedSheet_holder = pandas.ExcelFile(ScoreFilename)
PopulatedSheet = PopulatedSheet_holder.parse('Sheet1')

# If you didn't find a match, print something so that you can go back and manually fix the issue.
# This normally happens for teams like Southern Miss where one website calls them Southern Miss and the other calls them Southern Mississippi
for i in range(int(len(blanksheet)/2)):
	if pandas.isnull(PopulatedSheet.loc[i*2]["Score"]):
		Statement = "The matchup between " + PopulatedSheet.loc[i*2]["Matchup"] + " and " + PopulatedSheet.loc[i*2 + 1]["Matchup"] + " does not have a score!!"
		print(Statement)
