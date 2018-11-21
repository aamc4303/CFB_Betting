import requests
from bs4 import BeautifulSoup
import re
import xlsxwriter

Week = input("Week Number: ")
Excel_Filename = "CFB_Week" + str(Week) + "_FirstnameLastname.xlsx"

# Prepare the xlsx file
workbook = xlsxwriter.Workbook(Excel_Filename)
worksheet = workbook.add_worksheet()
Excel_row = 0

# Write the headers into the excel doc
worksheet.write(Excel_row,0, "Matchup")
worksheet.write(Excel_row,1, "Money Line")
worksheet.write(Excel_row,2, "Bet")
worksheet.write(Excel_row,3, "Spread")
worksheet.write(Excel_row,4, "Bet")
worksheet.write(Excel_row,5, "O/U")
worksheet.write(Excel_row,6, "Bet")
worksheet.write(Excel_row,8, "Total Bet:")
worksheet.write(Excel_row,9, '=sum(C:C,E:E,G:G)')

Excel_row = 1

# Read in the webpage with the spreads (you'll also use this page for team names, though that can be gathered from the spreads or moneyline pages
spreads_page = requests.get("http://www.donbest.com/ncaaf/odds/20181103.html")
spreads_soup = BeautifulSoup(spreads_page.text, 'html.parser')

team_name_list = spreads_soup.find_all(class_="oddsTeamWLink")
spreads_list = spreads_soup.find_all("div", {"id" : re.compile("_Div_Line_2_*")})

moneyline_page = requests.get("http://www.donbest.com/ncaaf/odds/money-lines/20181103.html")
moneyline_soup = BeautifulSoup(moneyline_page.text, 'html.parser')

moneylines_list = moneyline_soup.find_all("div", {"id" : re.compile("_Div_Line_2_*")})

i = 1
table_row = 1
index = 0
flag = 0

Bookie = int(input("Enter Bookie. (1) SC (2) Westgate (3) Mirage (4) Station (5) Pinnacle (6) SIA\n"))

Table_Offset = (7-Bookie)*2

for team_name_item in team_name_list:
	
	if flag == 1:
		flag = 0
		continue

	if i % 2 == 1:
		if table_row == 1:
			index = (10*table_row - Table_Offset)
		else:
			index = (10*table_row - Table_Offset) + 20*(table_row-1)
	else:
		if table_row == 1:
			index = (10*table_row - Table_Offset) + 1
		else:
			index = (10*table_row - Table_Offset) + 1 + 20*(table_row-1)
		table_row = table_row + 1
	# Check if the number you're reading is the 
	if spreads_list[index].text == '-':
		Statement = "Detected that there is not a spread or O/U in the game involving " + team_name_item.contents[0]
		print(Statement)
		if i % 2 == 1:
			i = i + 2
			table_row = table_row + 1
			flag = 1
		else:
			Excel_row = Excel_row - 1
			i = i + 1
			flag = 0
		continue

	elif moneylines_list[index].text == '-':
		Statement = "Detected that there is not a moneyline in the game involving " + team_name_item.contents[0]
		print(Statement)
		if i % 2 == 1:
			i = i + 2
			table_row = table_row + 1
			flag = 1
		else:
			Excel_row = Excel_row - 1
			i = i + 1
			flag = 0
		continue

	elif spreads_list[index].text == "PK":
		# The spread is a pick-em. To simplify, make the spread -0.5 and pray for no ties
		worksheet.write(Excel_row,0,team_name_item.contents[0])
		worksheet.write(Excel_row,1,moneylines_list[index].text)
		worksheet.write(Excel_row,2,"")
		worksheet.write(Excel_row,3,-0.5)
		worksheet.write(Excel_row,4,"")
		worksheet.write(Excel_row,5,"-")
		worksheet.write(Excel_row,6,"")


	elif float(spreads_list[index].text) > 0:
		# You've read the O/U
		OverUnder = float(spreads_list[index].text)
		
		worksheet.write(Excel_row,0,team_name_item.contents[0])
		worksheet.write(Excel_row,1,moneylines_list[index].text)
		worksheet.write(Excel_row,2,"")
		worksheet.write(Excel_row,3,"-")
		worksheet.write(Excel_row,4,"")
		worksheet.write(Excel_row,5,OverUnder)
		worksheet.write(Excel_row,6,"")

	elif float(spreads_list[index].text) < 0:
		# You've read the spread
		Spread = float(spreads_list[index].text)
		
		worksheet.write(Excel_row,0,team_name_item.contents[0])
		worksheet.write(Excel_row,1,moneylines_list[index].text)
		worksheet.write(Excel_row,2,"")
		worksheet.write(Excel_row,3,Spread)
		worksheet.write(Excel_row,4,"")
		worksheet.write(Excel_row,5,"-")
		worksheet.write(Excel_row,6,"")

	i = i + 1
	Excel_row = Excel_row + 1

# Format the Excel file to make it pretty
header_format = workbook.add_format()
header_format.set_bold(True)
header_format.set_font_size(12)
worksheet.set_row(0,10,header_format)

#even_matchup_format = workbook.add_format()
#even_matchup_format.set_bg_color("808080")

#odd_matchup_format = workbook.add_format()
#odd_matchup_format.set_bg_color("FFFFFF")
#
#flag = 'even matchup'
#flag_count = 0
#
#for i in range(200):
#
#	if i == 0:
#		continue
#
#	if flag == 'even matchup':	
#		worksheet.set_row(i,10,even_matchup_format)
#	elif flag == 'odd matchup':
#		worksheet.set_row(i,10,odd_matchup_format)
#	
#	if flag_count == 0:
#		flag_count = flag_count + 1
#	else:
#		flag_count = 0
#		if flag == 'even_matchup':
#			flag = 'odd_matchup'
#		else:
#			flag = 'even_matchup'
#


# Close your workbook
workbook.close()
