from bs4 import BeautifulSoup
import requests
#import re
#import xlsxwriter
#import pandas

#Week = 1
#Filename = 'CFB_Week' + str(Week) + '_Scores.xlsx'

#workbook = xlsxwriter(Filename)
#worksheet = workbook.add_worksheet()
#Excel_row = 0

# Get the scores page (this website must change for each week to match the week's scores. It will allow you to also read archived game scores)

scores_page = requests.get('https://www.sports-reference.com/cfb/boxscores/')
scores_soup = BeautifulSoup(scores_page.text, 'html.parser')

matchup_list = scores_soup.find_all(class_="teams")
#team_list = matchup_list.get('a')

print(matchup_list)

