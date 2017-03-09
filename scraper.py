# Scrapes data from basketball-reference.com for a given player

from lxml import html
import requests
import private

# playerName should be in format: "Firstname LastName"
# Example: "Lebron James"

# Globals:
headerFile = private.headerFile
startOfRow = private.startOfRow
endOfRow = private.endOfRow

def condensePage(page):
	indexOfStart = page.find(startOfRow)
	indexOfEnd = page.rfind(endOfRow)
	return page[indexOfStart:indexOfEnd]

def getStatsForPlayer(playerName, year):
	nameArr = playerName.split(' ')
	firstName = nameArr[0].lower()
	lastName = nameArr[1].lower()
	urlStr = private.getURL(firstName, lastName, year)

	# Retrieve the HTML page in a condensed form
	condensedPage = condensePage(requests.get(urlStr).content)
	tree = html.fromstring(condensedPage)

	# Retrieve the two forms of headers 
	file = open(headerFile)
	tableHeadersStr = file.readline()
	dataStatsStr = file.readline();
	tableHeaders = tableHeadersStr.replace(" ", "").strip().split(',')
	dataStats = dataStatsStr.replace(" ", "").strip().split(',')

	gameStats = []

	# Get number of games
	tempPath = private.getInitialPath(dataStats[0])
	numGames = len(tree.xpath(tempPath))

	# Traverse through games and retrieve all data
	lastIndex = 0
	rk = 1
	for count in range(0, numGames):
		dict = {}
		i = 0
		if condensedPage.find('<th', lastIndex+3) == -1:
			thisRow = condensedPage[lastIndex:]
		else:
			thisRow = condensedPage[lastIndex:condensedPage.find(startOfRow, lastIndex+len(startOfRow))]
		lastIndex = condensedPage.find(startOfRow, lastIndex+len(startOfRow))
		tree = html.fromstring(thisRow)
		for datastat in dataStats:
			if (datastat == 'ranker'):
				thisData = [str(rk)]
			else:
				xpathStr = private.getPath(datastat)
				thisData = tree.xpath(xpathStr)
			if (len(thisData) == 1):
				dict[tableHeaders[i]] = thisData[0]
			else:
				dict[tableHeaders[i]] = "N/A"
			i+=1
		gameStats.append(dict)
		rk+=1

	#for s in gameStats:
	#	print s
	#	print
	return gameStats


