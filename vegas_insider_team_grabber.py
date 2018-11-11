import requests
from bs4 import BeautifulSoup
import xlsxwriter

def ExtractSpreadTotal(lineString,lineType):

	# VegasInsider likes to use the special character for 1/2, but Python hates that character so replace it with an actual number
	if "½" in lineString:
		# Use a holder string to store your original lineString, then use replace to make a new lineString without the weird 1/2 character
		holderString = lineString
		lineString = holderString.replace("½",".5")
	# Get rid of non-breaking space that VegasInsider includes in their cells	
	if "\xa0" in lineString:
		holderString = lineString
		lineString = holderString.replace("\xa0"," ")
	i = 0

	# If you're extracting a spread, the lineType will be "S" for Spread
	if lineType == "S":
		
		# If it's a pick-em, just make it a line of -0.5 and pray that we won't have a tie
		if "PK" in lineString:
			return -0.5

		while lineString[i] != " ":
			i = i + 1

		Spread = float(lineString[:i])
		return Spread

	# "T" for Total
	elif lineType == "T":

		while lineString[i] != "u" and lineString[i] != "o":
			i = i + 1

		Total = float(lineString[:i])
		return Total

# Make a filename based on which week of the season it is
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

Excel_row = 1

spreads_page = requests.get("http://www.vegasinsider.com/college-football/odds/las-vegas/")
spreads_soup = BeautifulSoup(spreads_page.text, 'html.parser')

# Read in the webpage with the moneylines
moneylines_page = requests.get("http://www.vegasinsider.com/college-football/odds/las-vegas/money")
moneyline_soup = BeautifulSoup(moneylines_page.text, 'html.parser')

# You're going to parse through the huge table on the webpage so pull that out and separate by tr, or table rows
Master_Table_Spreads = spreads_soup.find("table", class_="frodds-data-tbl")
table_body_Spreads = Master_Table_Spreads.find_all('tr')

# Same idea with the money line table
Master_Table_Moneylines = moneyline_soup.find("table", class_="frodds-data-tbl")
table_body_Moneylines = Master_Table_Moneylines.find_all('tr')

# Index is critical. Must be kept accurate so that the moneyline and spread that you find apply to the same matchup
index = 0

for table in table_body_Spreads[:140]:
	
	# Write flag is used to tell if we have a spread, total, and moneyline. The flag will equal 2 if both criteria are met
	Write_Flag = 0
	
	team_name_list = table.find_all("a",class_="tabletext")
	
	if len(team_name_list) == 0:
		index += 1
		continue

	TeamNumber = 0
	Team = [[],[]]
	for teams in team_name_list:
		Team[TeamNumber] = teams.contents[0]
		TeamNumber += 1

	spreads_list = table.find_all(class_="viCellBg1 cellTextNorm cellBorderL1 center_text nowrap")
	spreads_list2 = table.find_all(class_="viCellBg2 cellTextNorm cellBorderL1 center_text nowrap")
	spreads_list.extend(spreads_list2)

	Desired_Spread_Column = 3
	Current_Spread_Column = 0
	for spreads in spreads_list:
		Current_Spread_Column = Current_Spread_Column + 1

		spread = str(spreads.find_all("a",class_="cellTextNorm"))

		if len(spread) > 2:
			Read_Flag = 0
			i = 0

                	# You're looking for 3 conditions, so don't stop the loop until you've met all 3
			while Read_Flag < 3:

				if spread[i:(i+4)] == "<br>" and Read_Flag == 0:
					FirstSpreadStart = i + 4
					Read_Flag = 1
				elif spread[i:(i+4)] == "<br>" and Read_Flag == 1:
					FirstSpreadEnd = i
					SecondSpreadStart = i + 4
					Read_Flag = 2
				elif spread[i:(i+5)] == "</br>" and Read_Flag == 2:
					SecondSpreadEnd = i
					Read_Flag = 3
				i = i + 1
			# Put the parsed strings into their own variables
			FirstSpreadString = spread[FirstSpreadStart:FirstSpreadEnd]
			SecondSpreadString = spread[SecondSpreadStart:SecondSpreadEnd]

			# Check to see if either spread string is missing a spread or total. All spreads and totals contain a '-' so check based on that
			if "-" not in FirstSpreadString and "-" not in SecondSpreadString:
				continue
			elif "u" not in FirstSpreadString and "u" not in SecondSpreadString and "o" not in FirstSpreadString and "o" not in SecondSpreadString:
				continue

			# Starting with the first spread string, check to see if it's a total or a spread. Totals will contain a 'u'
			if "u" in FirstSpreadString or "o" in FirstSpreadString:
				Total = [ExtractSpreadTotal(FirstSpreadString,"T"),0]
			else:
				Spread = [ExtractSpreadTotal(FirstSpreadString,"S"),0]

			if "u" in SecondSpreadString or "o" in SecondSpreadString:
				Total = [ExtractSpreadTotal(SecondSpreadString,"T"),1]
			else:
				Spread = [ExtractSpreadTotal(SecondSpreadString,"S"),1]
			
			if Current_Spread_Column == Desired_Spread_Column and Total != None and Spread != None:
				Write_Flag += 1
				break
	moneyline_list = table_body_Moneylines[index].find_all(class_="viCellBg1 cellTextNorm cellBorderL1 center_text nowrap")
	moneyline_list2 = table_body_Moneylines[index].find_all(class_="viCellBg2 cellTextNorm cellBorderL1 center_text nowrap")
	moneyline_list.extend(moneyline_list2)

	Desired_Moneyline_Column = Desired_Spread_Column
	Current_Moneyline_Column = 0

	for moneylines in moneyline_list:
		moneyline = str(moneylines.find_all("a",class_="cellTextNorm"))
		Current_Moneyline_Column += 1
		if len(moneyline) > 2:
			Read_Flag = 0
			i = 0

			while Read_Flag < 3:
				if moneyline[i:(i+4)] == "<br>" and Read_Flag == 0:
					FirstMoneylineStart = i + 4
					Read_Flag = 1
				elif moneyline[i:(i+4)] == "<br>" and Read_Flag == 1:
					FirstMoneylineEnd = i
					SecondMoneylineStart = i + 4
					Read_Flag = 2
				elif moneyline[i:(i+5)] == "</br>" and Read_Flag == 2:
					SecondMoneylineEnd = i
					Read_Flag = 3
				i = i + 1
			FirstMoneylineString = moneyline[FirstMoneylineStart:FirstMoneylineEnd]
			SecondMoneylineString = moneyline[SecondMoneylineStart:SecondMoneylineEnd]

			if len(FirstMoneylineString) < 3:
				continue
			elif len(SecondMoneylineString) < 3:
				continue
			
			if FirstMoneylineString[0] == "-":
				FirstMoneylineHolder = int(FirstMoneylineString[1:])
				FirstMoneylineString = "-" + str(FirstMoneylineHolder)
			else:
				FirstMoneylineHolder = int(FirstMoneylineString[1:])
				FirstMoneylineString = "+" + str(FirstMoneylineHolder)
			if SecondMoneylineString[0] == "-":
				SecondMoneylineHolder = int(SecondMoneylineString[1:])
				SecondMoneylineString = "-" + str(SecondMoneylineHolder)
			else:
				SecondMoneylineHolder = int(SecondMoneylineString)
				SecondMoneylineString = "+" + str(SecondMoneylineHolder)

			if len(FirstMoneylineString) > 1 and len(SecondMoneylineString) > 1:
				Team1Statement = "Moneyline on " + Team[0] + ": " + FirstMoneylineString
				Team2Statement = "Moneyline on " + Team[1] + ": " + SecondMoneylineString

				if Desired_Moneyline_Column == Current_Moneyline_Column:
					Write_Flag += 1
					break
	
	# If you have a total, spread, and moneyline, write the data to the excel file
	if Write_Flag == 2:
		worksheet.write(Excel_row,0,Team[0])
		worksheet.write(Excel_row+1,0,Team[1])
		worksheet.write(Excel_row,1,str(FirstMoneylineString))
		worksheet.write(Excel_row+1,1,str(SecondMoneylineString))
		worksheet.write(Excel_row,2,"")
		worksheet.write(Excel_row+1,2,"")
		worksheet.write(Excel_row,4,"")
		worksheet.write(Excel_row+1,4,"")
		worksheet.write(Excel_row,6,"")
		worksheet.write(Excel_row+1,6,"")

		if int(Spread[1]) == 0:
			worksheet.write(Excel_row,3,str(Spread[0]))
			worksheet.write(Excel_row+1,3,"-")
			worksheet.write(Excel_row,5,"-")
			worksheet.write(Excel_row+1,5,str(Total[0]))
		else:
			worksheet.write(Excel_row,3,"-")
			worksheet.write(Excel_row+1,3,str(Spread[0]))
			worksheet.write(Excel_row,5,str(Total[0]))
			worksheet.write(Excel_row+1,5,"-")
		Excel_row += 2

	Total = None
	Spread = None
	
	index += 1

EndStatement = "Total games collected: " + str((Excel_row - 3)/2)
print(EndStatement)
workbook.close()




