from tkinter import *
import random
import module_manager
import tkinter.font
import nltk
from nltk.corpus import wordnet as wn


module_manager.review()
#andrewid: hannahli
#112 TP!
####################################
# init
####################################


def readFile(path):
	#From 112 Lecture Notes
	with open(path, "rt") as f:
		return f.read()

def init(data):
	data.margin = 100
	data.numCells = 5
	#gameMode
	data.mode = "splashScreen"
	data.twentyFiveWords = []
	data.gameMap = [[0]*data.numCells for j in range(data.numCells)]
	loadGame(data)
	data.cellWidth = (data.width//data.numCells) - data.margin/2
	data.cellHeight = (data.height//data.numCells) -data.margin/2

	data.colors = {"startingColor":"#fcf9ef", "neutral":"#ede8d5", "red": "#bc4629", "blue": "#5b548e",
	"assassin": "#504f54"}
	data.isRedTurn = True
	data.font = tkinter.font.Font(family = "Raleway", size = 12)
	data.font2 = tkinter.font.Font(family = "Raleway ExtraBold", size = 11)
	data.fontTimer = tkinter.font.Font(family = "Raleway ExtraBold", size = 20)
	data.fontEnd = tkinter.font.Font(family = "Raleway ExtraBold", size = 40)
	data.time = 90
	data.singleTime = 0
	data.timerCalls = 0
	data.clueString = ""
	data.turnActive = True
	data.blueScore = 0
	data.redScore = 0
	data.clicksAllowed = 0

	data.winner = None
	data.singleClue = ""
	data.logo = PhotoImage(file='codenames_logo.gif')
	

#Round rectangle function from Stack Overflow: https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
def round_rectangle(canvas,x1, y1, x2, y2, radius=25, **kwargs):

    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)
	
def loadGame(data):
	data.wordBank = []
	ogWords = readFile("ogWords.txt")
	for word in ogWords.split("\n"):
		data.wordBank.append(word)
	generate25RandomWords(data)
	generateRandomMap(data)
	loadWords(data)

class Word():
	def __init__(self,value,allegiance,isClickedOn):
		self.value = value
		self.allegiance = allegiance
		self.isClickedOn = isClickedOn
	def __repr__(self):
		return self.value + "(" + self.allegiance + ")"

def generate25RandomWords(data):
	taken = set()
	#red team
	while len(data.twentyFiveWords) < data.numCells**2:
		index = random.randint(0, len(data.wordBank)-1)
		if index not in taken:
			taken.add(index)
			randWord = data.wordBank[index]
			randWordObject = Word(randWord, "yellow", False)
			data.twentyFiveWords.append(randWordObject)
	
def generateRandomMap(data):
	allegiances = (["red"] * 9) + (["blue"]*8) + (["neutral"] * 7) + (["assassin"]*1)
	for i in range(data.numCells):
		for j in range(data.numCells):
			item = allegiances[random.randint(0, len(allegiances)-1)]
			data.gameMap[i][j] = item
			allegiances.remove(item)

def loadWords(data):
	for i in range(data.numCells):
		for j in range(data.numCells):
			thisWord = data.twentyFiveWords.pop(0)
			thisWord.allegiance = data.gameMap[i][j]
			data.gameMap[i][j] = thisWord
	



####################################
# mode dispatcher
####################################

def mousePressed(event, data):
	#Calls correct mousePressed function
	if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
	elif (data.mode == "playGame"):   playGameMousePressed(event, data)
	elif (data.mode == "codemaster"):   codemasterMousePressed(event, data)
	elif (data.mode == "single"):   singleMousePressed(event, data)
	elif (data.mode == "end"):       endMousePressed(event, data)
	elif (data.mode == "singleEnd"):       singleEndMousePressed(event, data)


def keyPressed(event, data):
	#Calls correct keyPressed function
	if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
	elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
	elif (data.mode == "codemaster"):	codemasterKeyPressed(event, data)
	elif (data.mode == "single"):	singleKeyPressed(event, data)
	elif (data.mode == "end"):       endKeyPressed(event, data)
	elif (data.mode == "singleEnd"):       singleEndKeyPressed(event, data)

def timerFired(data):
	#calls correct timerFired function
	if (data.mode == "splashScreen"): splashScreenTimerFired(data)
	elif (data.mode == "playGame"):   playGameTimerFired(data)
	elif (data.mode == "codemaster"):	codemasterTimerFired(data)
	elif (data.mode == "single"):	singleTimerFired(data)
	elif (data.mode == "end"):       endTimerFired(data)
	elif (data.mode == "singleEnd"):       singleEndTimerFired(data)

def redrawAll(canvas, data):
	#calls correct redrawAll function
	if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
	elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
	elif (data.mode == "codemaster"):	codemasterRedrawAll(canvas, data)
	elif (data.mode == "single"):   singleRedrawAll(canvas, data)
	elif (data.mode == "end"):       endRedrawAll(canvas, data)
	elif (data.mode == "singleEnd"):       singleEndRedrawAll(canvas, data)

####################################
# splashScreen mode
####################################

def splashScreenMousePressed(event, data):
	#No mousepressed action
	if (event.x > data.width/2 - 100) and(event.x < data.width/2 + 100) and(event.y > data.height/2 + 175) and(event.y < data.height/2 + 225):
			data.mode = "codemaster"

	elif (event.x > data.width/2 - 100) and(event.x < data.width/2 + 100) and(event.y > data.height/2 + 100) and(event.y < data.height/2 + 150):
			data.mode = "single"
def splashScreenKeyPressed(event, data):
	#Start game when p is pressed
	pass


def splashScreenTimerFired(data):
	pass


def splashScreenRedrawAll(canvas, data):
	#Draws everything on the splash screen
	
					   
	canvas.create_rectangle(data.width/2 - 100, data.height/2 + 150, data.width/2 + 100, 
		data.height/2 + 100,outline = "white", fill = data.colors["red"])

	canvas.create_text(data.width/2, data.height/2 + 125, text = "single player", font = data.font)

	canvas.create_rectangle(data.width/2 - 100, data.height/2 + 225, data.width/2 + 100, 
		data.height/2 + 175,outline = "white", fill = data.colors["blue"])

	canvas.create_text(data.width/2, data.height/2 + 200, text = "multiplayer", font = data.font)
	textentry = Entry(canvas)

	

	canvas.create_image(data.width/2, data.height/3, anchor = CENTER, image = data.logo)
	canvas.create_text(data.width/2, data.height/2+20,
					   text="112 Edition!", font = data.fontTimer, fill = data.colors["red"])

	canvas.create_text(data.width/2, data.height/2+70,
					   text="For multiplayer, start by giving the screen to the red team's codemaster!", font = data.font, fill = data.colors["assassin"])
	canvas.create_text(data.width/2, data.height/2+50,
					   text="Must have Python NLTK installed.", font = data.font, fill = data.colors["assassin"])

####################################
# end mode
####################################

def endMousePressed(event, data):
	#No mousePressed action
	pass

def endKeyPressed(event, data):
	#Restarts when S is pressed
	if event.char == "s":
		data.mode = "splashScreen"

		init(data)

def endTimerFired(data):
	#No timerFired action
	pass

def endRedrawAll(canvas, data):
	#Draws everything in end state
	canvas.create_rectangle(0,0,data.width,data.height,
					   fill = data.colors["neutral"])
	if data.winner == "red":
		canvas.create_text(data.width/2, data.height/2-10,
					   text="RED TEAM WINS!", font= data.fontEnd,  fill = data.colors["red"])	
	elif data.winner == "blue":
		canvas.create_text(data.width/2, data.height/2-10,
					   text="BLUE TEAM WINS!", font= data.fontEnd,  fill = data.colors["blue"])
	
	canvas.create_text(data.width/2, data.height/2+40,
					   text="Press 's' to play again!", fill = data.colors["blue"],font= data.fontTimer)
####################################
# singleplayer end mode
####################################

def singleEndMousePressed(event, data):
	#No mousePressed action
	pass

def singleEndKeyPressed(event, data):
	#Restarts when S is pressed
	if event.char == "s":
		data.mode = "splashScreen"
	init(data)


def singleEndTimerFired(data):
	#No timerFired action
	pass

def singleEndRedrawAll(canvas, data):
	#Draws everything in end state
	canvas.create_rectangle(0,0,data.width,data.height,
					   fill = data.colors["neutral"])

	canvas.create_text(data.width/2, data.height/2-10,
		text="You won in "+str(data.singleTime) + " seconds!", font= data.fontEnd,  fill = data.colors["red"])	

	canvas.create_text(data.width/2, data.height/2+40,
					   text="Press 's' to play again!", fill = data.colors["blue"],font= data.fontTimer)
####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
	if (event.x > data.width/2 + 200) and(event.x < data.width/2 + 300) and(event.y > data.height/2 + 250) and(event.y < data.height/2 + 300):
			data.mode = "codemaster"
			data.isRedTurn = not data.isRedTurn
			data.time = 90
			data.clueString = ""
	elif data.turnActive and event.x > data.margin and event.x < data.margin + data.cellWidth*data.numCells:
		if event.y > data.margin and event. y < data.margin + data.cellHeight*data.numCells:
			row = (event.y - data.margin) // data.cellHeight
			col = (event.x - data.margin)// data.cellWidth
			clickedWord = data.gameMap[int(row)][int(col)]
			clickedWord.isClickedOn = True
			if clickedWord.allegiance == "red" and not data.isRedTurn:
				data.turnActive = False
				data.redScore += 1
			elif clickedWord.allegiance == "blue" and data.isRedTurn:
				data.turnActive = False
				data.blueScore +=1
			elif clickedWord.allegiance == "neutral":
				data.turnActive = False
			elif clickedWord.allegiance == "assassin":
				data.turnActive = False
				data.mode = "end"
			else:
				if data.isRedTurn:
					data.redScore += 1
				else:
					data.blueScore += 1

			data.clicksAllowed -= 1
			
	if data.clicksAllowed < 1:
		data.turnActive = False

	if data.redScore == 9:
		data.mode = "end"
		data.winner = "red"
	elif data.blueScore == 8:
		data.mode = "end"
		data.winner = "blue"
		


def playGameKeyPressed(event, data):
	#Scrolls screen around when arrow keys pressed
	pass


def playGameTimerFired(data):
	if data.timerCalls % 10 == 0: #Every second
		data.time -= 1
	data.timerCalls += 1
	if data.time < 1:
		data.mode = "end"
	
def drawBoard(canvas, data):

	
	for row in range(data.numCells):
		for col in range(data.numCells):
			left = (col*data.cellWidth) + data.margin/4
			top = (row*data.cellHeight)
			myWord = data.gameMap[row][col]

			color = data.colors[myWord.allegiance]
			if myWord.isClickedOn:
				round_rectangle(canvas,data.margin+left, data.margin+top, data.margin+left+data.cellWidth, data.margin+top+data.cellHeight, radius=20, fill=color, outline = "white", width = 4)
			else:
				round_rectangle(canvas,data.margin+left, data.margin+top, data.margin+left+data.cellWidth, data.margin+top+data.cellHeight, radius=20, fill=data.colors["startingColor"], outline = "white", width = 4)
			canvas.create_text(data.margin+left+data.cellWidth/2, data.margin+top+data.cellHeight/2,
					text = myWord.value, fill ="black", font = data.font2)


def playGameRedrawAll(canvas, data):
	#Draws everything in game mode
	drawBoard(canvas,data)

	canvas.create_rectangle(data.width/2+190 , data.height/2+250, data.width/2+310, 
		data.height/2 + 300,outline = "white", fill = data.colors["assassin"])

	canvas.create_text(data.width/2, data.height/2 +275,
						text = str(data.time), font=data.fontTimer)

	canvas.create_text(data.width/2 + 250, data.height/2 + 275, text = "Codemaster", font = data.font)
	if data.isRedTurn:
		canvas.create_text(data.width/2, data.height/2 + 225, text = "Red team, your clue is: " + data.textEntry.get(), font = data.font, fill = data.colors["red"])
	else:
		canvas.create_text(data.width/2, data.height/2 + 225, text = "Blue team, your clue is: " + data.textEntry.get(), font = data.font, fill = data.colors["blue"])
	canvas.create_text(data.width/2 + 300, 20, text = data.redScore, fill = data.colors["red"], font = data.fontTimer)
	canvas.create_text(data.width/2 - 300, 20, text = data.blueScore, fill = data.colors["blue"], font = data.fontTimer)
####################################
# codemaster mode
####################################

def codemasterMousePressed(event, data):
	if (event.x > data.width/2 + 200) and(event.x < data.width/2 + 300) and(event.y > data.height/2 + 250) and(event.y < data.height/2 + 300) and len(data.clueString) > 0:
			data.mode = "playGame"
			data.turnActive = True
			data.clicksAllowed = int(data.clueString[-1]) + 1
		

def codemasterKeyPressed(event, data):
	if event.keysym == "BackSpace":
		data.clueString = data.clueString[:len(data.clueString)-1]
	else:
		data.clueString += event.char



def codemasterTimerFired(data):

	if data.timerCalls % 10 == 0: #Every second
		data.time -= 1
	data.timerCalls += 1

	if data.time < 1:
		data.mode = "end"
	

def codemasterDrawBoard(canvas, data):
	for row in range(data.numCells):
		for col in range(data.numCells):
			left = (col*data.cellWidth) + data.margin/4
			top = (row*data.cellHeight)
			myWord = data.gameMap[row][col]

			color = data.colors[myWord.allegiance]

			round_rectangle(canvas,data.margin+left, data.margin+top, data.margin+left+data.cellWidth, data.margin+top+data.cellHeight, radius=20, fill=color, outline = "white", width = 4)

			canvas.create_text(data.margin+left+data.cellWidth/2, data.margin+top+data.cellHeight/2,
					text = myWord.value, fill ="black", font = data.font2)
def codemasterRedrawAll(canvas, data):
	codemasterDrawBoard(canvas,data)

	canvas.create_rectangle(data.width/2+190 , data.height/2+250, data.width/2+310, 
		data.height/2 + 300,outline = "white", fill = data.colors["assassin"])
	canvas.create_text(data.width/2, data.height/2 +275,
						text = str(data.time), font=data.fontTimer)

	canvas.create_text(data.width/2 + 250, data.height/2 + 275, text = "Player", font = data.font)
	data.textEntry = Entry(canvas)

	data.textEntry.insert(0, data.clueString)
	canvas.create_window(data.width/2, data.height/2 + 220, window=data.textEntry, height=20, width=300)

	canvas.create_text(data.width/2 + 300, 20, text = data.redScore, fill = data.colors["red"], font = data.fontTimer)
	canvas.create_text(data.width/2 - 300, 20, text = data.blueScore, fill = data.colors["blue"], font = data.fontTimer)

	if data.isRedTurn:
		canvas.create_text(data.width/2, 40, text = "Red Codemaster, type in a clue!", fill = data.colors["red"], font = data.fontTimer)
	else:
		canvas.create_text(data.width/2, 40, text = "Blue Codemaster, type in a clue!", fill = data.colors["blue"], font = data.fontTimer)
####################################
# single mode
####################################


def singleGenerateWordList(data):

	singleWordStrings = []
	for row in range(data.numCells):
		for col in range(data.numCells):
			myWord = data.gameMap[row][col]
			if myWord.allegiance == "red" and not myWord.isClickedOn:
				singleWordStrings.append(myWord.value)
	print(singleWordStrings)
	return singleWordStrings

#From NLTK tutorial
def polysemy(word):
        return len(wn.synsets(word))

def singleGenerateClues(data):
	if len(singleGenerateWordList(data)) == 1:
		clues = singleGenerateWordList(data)[0]
	else:

		clues = random.sample(singleGenerateWordList(data),2)
	word1 = random.choice(clues)
	clues.remove(word1)
	word2 = clues[0]


	sense1 = "0" + str(random.randint(1, 3))
	sense2 = "0" + str(random.randint(1, 3))
	try:
		try:
			synset1 = wn.synset(word1+".n." + sense1)
		except:
			try: 
				synset1 = wn.synset(word1+".n.01")
			except:
				synset1 = wn.synset(word1+".v." + sense1)
		try:
			synset2 = wn.synset(word2 +".n." + sense2)
		except:
			try: 
				synset2 = wn.synset(word2+".n.01")
			except:
				synset2 = wn.synset(word2+".v." + sense1)
	except:
		return "JUST GUESS"


	hypernyms = synset1.hypernyms()
	hyponyms = synset1.hyponyms()

	related = hypernyms + hyponyms
	maxSimilarity = 0
	mostSimilar = None
	for item in related:

		mySimilarity = synset2.wup_similarity(synset1)
		if mySimilarity > maxSimilarity:
			maxSimilarity = mySimilarity
			mostSimilar = item

	return(str(mostSimilar)[8:-7])




def singleMousePressed(event, data):
	if (event.x > data.width/2 + 200) and(event.x < data.width/2 + 300) and(event.y > data.height/2 + 250) and(event.y < data.height/2 + 300):
		data.turnActive = True
		data.singleClue = singleGenerateClues(data)
		

	if data.turnActive and event.x > data.margin and event.x < data.margin + data.cellWidth*data.numCells:
		if event.y > data.margin and event. y < data.margin + data.cellHeight*data.numCells:
			row = (event.y - data.margin) // data.cellHeight
			col = (event.x - data.margin)// data.cellWidth
			clickedWord = data.gameMap[int(row)][int(col)]
			clickedWord.isClickedOn = True

			if clickedWord.allegiance == "red":
				data.redScore += 1
			else:
				data.turnActive = False
	if data.redScore == 9:
		data.mode = "singleEnd"
		

def singleKeyPressed(event, data):
	#Scrolls screen around when arrow keys pressed
	pass


def singleTimerFired(data):
	if data.timerCalls % 10 == 0: #Every second
		data.singleTime += 1
	data.timerCalls += 1

	

def singleDrawBoard(canvas,data):
	for row in range(data.numCells):
		for col in range(data.numCells):
			left = (col*data.cellWidth) + data.margin/4
			top = (row*data.cellHeight)
			myWord = data.gameMap[row][col]

			color = data.colors[myWord.allegiance]
			if myWord.isClickedOn:
				round_rectangle(canvas,data.margin+left, data.margin+top, data.margin+left+data.cellWidth, data.margin+top+data.cellHeight, radius=20, fill=color, outline = "white", width = 4)
			else:
				round_rectangle(canvas,data.margin+left, data.margin+top, data.margin+left+data.cellWidth, data.margin+top+data.cellHeight, radius=20, fill=data.colors["startingColor"], outline = "white", width = 4)
			canvas.create_text(data.margin+left+data.cellWidth/2, data.margin+top+data.cellHeight/2,
					text = myWord.value, fill ="black", font = data.font2)
	

def singleRedrawAll(canvas, data):
	#Draws everything in game mode
	singleDrawBoard(canvas,data)
	canvas.create_text(data.width/2, data.height/2 +275,
						text = str(data.singleTime), font=data.fontTimer)
	

	canvas.create_rectangle(data.width/2+190 , data.height/2+250, data.width/2+310, 
		data.height/2 + 300,outline = "white", fill = data.colors["assassin"])


	canvas.create_text(data.width/2 + 250, data.height/2 + 275, text = "Clue", font = data.font)
	canvas.create_text(data.width/2, 15, text = data.redScore, fill = data.colors["red"], font = data.fontTimer)
	canvas.create_text(data.width/2, data.height/2 + 225, text = "Your clue is: " + data.singleClue, font = data.font, fill = data.colors["red"])
####################################
# Run function from 112 Course Notes
####################################

def run(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds
	root = Tk()
	root.resizable(width=False, height=False) # prevents resizing window
	init(data)
	# create the root and the canvas
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.configure(bd=0, highlightthickness=0)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(1100, 700)