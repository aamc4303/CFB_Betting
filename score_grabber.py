from bs4 import BeautifulSoup
import requests
import xlsxwriter
import pandas

Week = input("Week Number: ")

# Establish your two file names. The blank file is the file without the bets but with the matchups included
ScoreFilename = "CFB_Week" + str(Week) + "_Scores.xlsx"
BlankFilename = "CFB_Week" + str(Week) + "_FirstnameLastname.xlsx"

# Create your scores excel file for the week
ScoreWorkbook = xlsxwriter.Workbook(ScoreFilename)
ScoreWorksheet = ScoreWorkbook.add_worksheet()
Excel_row = 0

# Write the headers to the score file
ScoreWorksheet.write(0,0,"Matchup")
ScoreWorksheet.write(0,1,"Score")

blank_holder = pandas.ExcelFile(BlankFilename)
blanksheet = blank_holder.parse('Sheet1')

for i in range(int(len(blanksheet)/2)):
	Excel_row = i*2
	Team1 = blanksheet.loc[i*2]['Matchup']
	Team2 = blanksheet.loc[i*2 + 1]['Matchup']

	ScoreWorksheet.write(Excel_row + 1,0,Team1)
	ScoreWorksheet.write(Excel_row + 2,0,Team2)

	

# Get the scores page (this website must change for each week to match the week's scores. It will allow you to also read archived game scores)

scores_page = requests.get('https://www.sports-reference.com/cfb/boxscores/')
scores_soup = BeautifulSoup(scores_page.text, 'html.parser')

matchup_tables = scores_soup.find_all('table', {'class':"teams"})

for i in range(len(matchup_tables)):
	
	matchup = matchup_tables[i].select("a")
	score = matchup_tables[i].find_all(class_="right")
#	print(matchup[0].text)
#	print(score[0].text)
#	print(matchup[2].text)
#	print(score[2].text)

	write_flag = 0
	
	for j in range(int(len(blanksheet)/2)):
		if blanksheet.loc[j*2]['Matchup'] == matchup[0].text or blanksheet.loc[j*2+1]['Matchup'] == matchup[2].text:
			ScoreWorksheet.write(j*2 + 1,1,score[0].text)
			ScoreWorksheet.write(j*2 + 2,1,score[2].text)
			write_flag = 1
		elif blanksheet.loc[j*2 + 1]['Matchup'] == matchup[0].text or blanksheet.loc[j*2]['Matchup'] == matchup[2].text:
			ScoreWorksheet.write(j*2 + 1,1,score[2].text)
			ScoreWorksheet.write(j*2 + 2,1,score[0].text)
			write_flat = 1

	if write_flag == 0:
		Statement = matchup[0].text + "and " + matchup[2].text + " could not be matched with any teams in the worksheet"
		print(Statement)
	else:
		Statement = matchup[0].text + "and " + matchup[2].text + " name identified and score saved"
		print(Statement)


ScoreWorkbook.close()

