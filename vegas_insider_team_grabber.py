"""
This script goes online to pull the most up-to-date college football betting
lines from vegasinsider.com. It puts those lines into an Excel file which is
then sent to every participant to fill out.
"""

import requests
from bs4 import BeautifulSoup
import xlsxwriter

# Spreads and Totals are saved with relatively difficult text formatting. This function extracts the meat from the fluff in the spread and total cells in the table
def ExtractSpreadTotal(lineString,lineType):

    # VegasInsider likes to use the special character for 1/2, but Python hates that character so replace it with an actual number
    if "½" in lineString:
        # Use a holder string to store your original lineString, then use replace to make a new lineString without the weird 1/2 character
        holderString = lineString
        lineString = holderString.replace("½",".5")
    # Get rid of non-breaking space that VegasInsider includes in some of their cells    
    if "\xa0" in lineString:
        holderString = lineString
        lineString = holderString.replace("\xa0"," ")
    i = 0

    # If you're extracting a spread, the lineType will be "S" for Spread
    if lineType == "S":
        
        # If it's a pick-em, just make it a line of -0.5 and pray that we won't have a tie
        if "PK" in lineString:
            return -0.5

        # Parse through the lineString until you find a space. The space indicates the end of the text for the line
        while lineString[i] != " ":
            i = i + 1

        # Use your knowledge of the end of the text to save the important part as the spread. Save as a float so that half-point spreads aren't truncated
        spread = float(lineString[:i])
        return spread

    # "T" for Total
    elif lineType == "T":

        # VegasInsider puts "u" and "o" at the end of the text showing the line total
        while lineString[i] != "u" and lineString[i] != "o":
            i = i + 1

        # Save the total using your knowledge of where the text containing total information lies
        total = float(lineString[:i])
        return total

# Make a filename based on which week of the season it is
Week = input("Week Number: ")
Excel_Filename = "CFB_Week" + str(Week) + "_FirstnameLastname.xlsx"

# Prepare the xlsx file
workbook = xlsxwriter.Workbook(Excel_Filename)
worksheet = workbook.add_worksheet()
excelRow = 0

# Write the headers into the excel doc
worksheet.write(excelRow,0, "Matchup")
worksheet.write(excelRow,1, "Money Line")
worksheet.write(excelRow,2, "Bet")
worksheet.write(excelRow,3, "Spread")
worksheet.write(excelRow,4, "Bet")
worksheet.write(excelRow,5, "O/U")
worksheet.write(excelRow,6, "Bet")
worksheet.write(excelRow,8, "Total Bet:")
worksheet.write(excelRow,9, '=sum(C:C,E:E,G:G)')

# Increment the row to be the 2nd in the file. You're done with headers and are ready to insert quality data
excelRow = 1

# Use the requests package to pull the html data from VegasInsider. This page contains the information about the spreads for the games
spreadsPage = requests.get("http://www.vegasinsider.com/college-football/odds/las-vegas/")
spreadsSoup = BeautifulSoup(spreadsPage.text, 'html.parser')

# Read in the webpage with the moneyline in the same way
moneylinesPage = requests.get("http://www.vegasinsider.com/college-football/odds/las-vegas/money")
moneylineSoup = BeautifulSoup(moneylinesPage.text, 'html.parser')

# You're going to parse through the huge table on the webpage so pull that out and separate by tr, or table rows
masterTableSpreads = spreadsSoup.find("table", class_="frodds-data-tbl")
tableBodySpreads = masterTableSpreads.find_all('tr')

# Same idea with the money line table
masterTableMoneylines = moneylineSoup.find("table", class_="frodds-data-tbl")
tableBodyMoneylines = masterTableMoneylines.find_all('tr')

# Index is critical. Must be kept accurate so that the moneyline and spread that you find apply to the same matchup
index = 0

# Parse through every row of the massive table from the site containing the spreads
for tableRow in tableBodySpreads:
    
    # writeFlag is used to tell if we have a spread, total, and moneyline. The flag will equal 2 if both criteria are met.
    writeFlag = 0
    
    # Pull the team names from the table row
    teamNameList = tableRow.find_all("a",class_="tabletext")
    
    # If the row does not contain any team names, skip the row because it won't contain any spreads or moneylines and will generally cause chaos
    if len(teamNameList) == 0:
        index += 1
        continue

    # Pull the team names from the teamNameList
    teamNumber = 0
    team = [[],[]]
    for teams in teamNameList:
        # teams will contain several items, but you just want the text for the team name so extract the text only
        team[teamNumber] = teams.contents[0]
        teamNumber += 1

    # For some reason, two different classes are used for spreads. Pull both and then combine
    spreadsList = tableRow.find_all(class_="viCellBg1 cellTextNorm cellBorderL1 center_text nowrap")
    spreadsList2 = tableRow.find_all(class_="viCellBg2 cellTextNorm cellBorderL1 center_text nowrap")
    spreadsList.extend(spreadsList2)

    # The desired spread column currently corresponds with the Westgate Sportsbook. Changing the desired column will change which sportsbook you prefer to get the lines from
    desiredSpreadColumn = 2
    currentSpreadColumn = 0
    
    # Go through every spread in the current row (ie the current matchup)
    for spreads in spreadsList:
        
        currentSpreadColumn += 1

        # Extract the spread from the crowded spreads item
        spread = str(spreads.find_all("a",class_="cellTextNorm"))

        # If the length of spread is greater than 2, a spread for the matchup exists
        if len(spread) > 2:

            # There are two different formats that spreads and totals are saved in. Determine which format you're dealing with
            if "<br/>" in spread:
                # Determine where in the spread string the relevant strings start and stop
                firstSpreadStart = spread.find("<br/>") + 5
                firstSpreadEnd = spread.find("<br/>",firstSpreadStart)
                secondSpreadStart = firstSpreadEnd + 5
                secondSpreadEnd = spread.find("</a>",secondSpreadStart)
            elif "<br>" in spread:
                # Determine where in the spread string the relevant strings start and stop
                firstSpreadStart = spread.find("<br>") + 4
                firstSpreadEnd = spread.find("<br>",firstSpreadStart)
                secondSpreadStart = firstSpreadEnd + 4
                secondSpreadEnd = spread.find("</br>",secondSpreadStart)

            # Put the two spread strings into their own variables using the knowledge of where the strings start and stop
            firstSpreadString = spread[firstSpreadStart:firstSpreadEnd]
            secondSpreadString = spread[secondSpreadStart:secondSpreadEnd]

            # Check to see if either spread string is missing a spread or total, or contains garbage. If so, skip this item and move on to the next
            if "-" not in firstSpreadString and "-" not in secondSpreadString:
                continue
            elif "u" not in firstSpreadString and "u" not in secondSpreadString and "o" not in firstSpreadString and "o" not in secondSpreadString:
                continue
            elif firstSpreadString[:2] == "XX" or secondSpreadString[:2] == "XX":
                continue

            # Starting with the first spread string, check to see if it's a total or a spread. Totals will contain a 'u' or an 'o'
            if "u" in firstSpreadString or "o" in firstSpreadString:
                total = [ExtractSpreadTotal(firstSpreadString,"T"),0]
            # If it isn't a total, it's a spread
            else:
                spread = [ExtractSpreadTotal(firstSpreadString,"S"),0]

            if "u" in secondSpreadString or "o" in secondSpreadString:
                total = [ExtractSpreadTotal(secondSpreadString,"T"),1]
            else:
                spread = [ExtractSpreadTotal(secondSpreadString,"S"),1]
            
            # If this spread comes from the column that you wanted to read from, set the write flag and stop reading more from this row because you already have what you want
            if currentSpreadColumn == desiredSpreadColumn and total != None and spread != None:
                writeFlag += 1
                break
            
    moneylineList = tableBodyMoneylines[index].find_all(class_="viCellBg1 cellTextNorm cellBorderL1 center_text nowrap")
    moneylineList2 = tableBodyMoneylines[index].find_all(class_="viCellBg2 cellTextNorm cellBorderL1 center_text nowrap")
    moneylineList.extend(moneylineList2)

    desiredMoneylineColumn = desiredSpreadColumn
    currentMoneylineColumn = 0

    for moneylines in moneylineList:
        moneyline = str(moneylines.find_all("a",class_="cellTextNorm"))
        currentMoneylineColumn += 1
        if len(moneyline) > 2:
            
            # There are two different formats that spreads and totals are saved in. Determine which format you're dealing with
            if "<br/>" in moneyline:
                # Determine where in the moneyline string the relevant strings start and stop
                firstMoneylineStart = moneyline.find("<br/>") + 5
                firstMoneylineEnd = moneyline.find("<br/>",firstMoneylineStart)
                secondMoneylineStart = firstMoneylineEnd + 5
                secondMoneylineEnd = moneyline.find("</a>",secondMoneylineStart)
            elif "<br>" in moneyline:
                # Determine where in the moneyline string the relevant strings start and stop
                firstMoneylineStart = moneyline.find("<br>") + 4
                firstMoneylineEnd = moneyline.find("<br>",firstMoneylineStart)
                secondMoneylineStart = firstMoneylineEnd + 4
                secondMoneylineEnd = moneyline.find("</br>",secondMoneylineStart)

            # Create moneyline strings using the knowledge of the location of the strings in the larger moneyline strings
            firstMoneylineString = moneyline[firstMoneylineStart:firstMoneylineEnd]
            secondMoneylineString = moneyline[secondMoneylineStart:secondMoneylineEnd]

            # Moneyline strings MUST be greater than 2 chars long. If they are not, there likely isn't a moneyline for this matchup so you should move on
            if len(firstMoneylineString) < 3 or len(secondMoneylineString) < 3:
                continue
            
            # Perform some gymnastics to ensure that the "-" and "+" signs get carried over to the Excel file
            if firstMoneylineString[0] == "-":
                firstMoneylineHolder = int(firstMoneylineString[1:])
                firstMoneylineString = "-" + str(firstMoneylineHolder)
            else:
                firstMoneylineHolder = int(firstMoneylineString[1:])
                firstMoneylineString = "+" + str(firstMoneylineHolder)
            if secondMoneylineString[0] == "-":
                secondMoneylineHolder = int(secondMoneylineString[1:])
                secondMoneylineString = "-" + str(secondMoneylineHolder)
            else:
                secondMoneylineHolder = int(secondMoneylineString)
                secondMoneylineString = "+" + str(secondMoneylineHolder)

            # If you have the moneyline from the sportsbook that you care about, stop looking for more moneylines because you have what you need
            if desiredMoneylineColumn == currentMoneylineColumn:
                writeFlag += 1
                break
    
    # If you have a total, spread, and moneyline, write the data to the excel file
    if writeFlag == 2:
        worksheet.write(excelRow,0,team[0])
        worksheet.write(excelRow+1,0,team[1])
        worksheet.write(excelRow,1,str(firstMoneylineString))
        worksheet.write(excelRow+1,1,str(secondMoneylineString))
        worksheet.write(excelRow,2,"")
        worksheet.write(excelRow+1,2,"")
        worksheet.write(excelRow,4,"")
        worksheet.write(excelRow+1,4,"")
        worksheet.write(excelRow,6,"")
        worksheet.write(excelRow+1,6,"")

        # If the spread is on the first team, write the spread next to the first team's name
        if int(spread[1]) == 0:
            worksheet.write(excelRow,3,str(spread[0]))
            worksheet.write(excelRow+1,3,"-")
            worksheet.write(excelRow,5,"-")
            worksheet.write(excelRow+1,5,str(total[0]))
        # Otherwise the second team has the spread on their name
        else:
            worksheet.write(excelRow,3,"-")
            worksheet.write(excelRow+1,3,str(spread[0]))
            worksheet.write(excelRow,5,str(total[0]))
            worksheet.write(excelRow+1,5,"-")
        excelRow += 2

    # Clear the total and spread items before you start looking at the next matchup
    total = None
    spread = None
    
    # Increment the index to the next matchup
    index += 1

# Brag
endStatement = "Total games collected: " + str((excelRow - 3)/2)
print(endStatement)

# Close the workbook like a good programmer
workbook.close()

