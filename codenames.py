from tkinter import *
import random
import module_manager
import tkinter.font

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
	data.time = 90
	data.timerCalls = 0
	data.clueString = ""
	data.turnActive = True
	data.blueScore = 0
	data.redScore = 0
	data.clicksAllowed = 0

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


def keyPressed(event, data):
	#Calls correct keyPressed function
	if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
	elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
	elif (data.mode == "codemaster"):	codemasterKeyPressed(event, data)
	elif (data.mode == "single"):	singleKeyPressed(event, data)
	elif (data.mode == "end"):       endKeyPressed(event, data)

def timerFired(data):
	#calls correct timerFired function
	if (data.mode == "splashScreen"): splashScreenTimerFired(data)
	elif (data.mode == "playGame"):   playGameTimerFired(data)
	elif (data.mode == "codemaster"):	codemasterTimerFired(data)
	elif (data.mode == "single"):	singleTimerFired(data)
	elif (data.mode == "end"):       endTimerFired(data)

def redrawAll(canvas, data):
	#calls correct redrawAll function
	if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
	elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
	elif (data.mode == "codemaster"):	codemasterRedrawAll(canvas, data)
	elif (data.mode == "single"):   singleRedrawAll(canvas, data)
	elif (data.mode == "end"):       endRedrawAll(canvas, data)


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
	canvas.create_text(data.width/2, data.height/2-50,
					   text="112 Codenames!", font = data.font)

	canvas.create_text(data.width/2, data.height/2+20,
					   text="Select your playing mode:", font = data.font)				   
	canvas.create_rectangle(data.width/2 - 100, data.height/2 + 150, data.width/2 + 100, 
		data.height/2 + 100,outline = "white", fill = "#b3dd82")

	canvas.create_text(data.width/2, data.height/2 + 125, text = "single player", font = data.font)

	canvas.create_rectangle(data.width/2 - 100, data.height/2 + 225, data.width/2 + 100, 
		data.height/2 + 175,outline = "white", fill = "#ddc382")

	canvas.create_text(data.width/2, data.height/2 + 200, text = "multiplayer", font = data.font)
	textentry = Entry(canvas)

	

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

def endTimerFired(data):
	#No timerFired action
	pass

def endRedrawAll(canvas, data):
	#Draws everything in end state
	canvas.create_rectangle(0,0,data.width,data.height,
					   fill = "red")
	canvas.create_text(data.width/2, data.height/2-10,
					   text="GAME OVER!:", font="Arial 20", fill = "white")
	canvas.create_text(data.width/2, data.height/2+15,
					   text="Final Score:"+str(data.score), font="Arial 20", 
					   fill = "white")
	canvas.create_text(data.width/2, data.height/2+40,
					   text="Press 's' to play again!", font="Arial 20", 
					   fill ="white")

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

	canvas.create_rectangle(data.width/2+200 , data.height/2+250, data.width/2+300, 
		data.height/2 + 300,outline = "white", fill = "#42cbf4")

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

	canvas.create_rectangle(data.width/2+200 , data.height/2+250, data.width/2+300, 
		data.height/2 + 300,outline = "white", fill = "#42cbf4")
	canvas.create_text(data.width/2, data.height/2 +275,
						text = str(data.time), font=data.fontTimer)

	canvas.create_text(data.width/2 + 250, data.height/2 + 275, text = "Player", font = data.font)
	data.textEntry = Entry(canvas)

	data.textEntry.insert(0, data.clueString)
	canvas.create_window(data.width/2, data.height/2 + 220, window=data.textEntry, height=20, width=300)

	canvas.create_text(data.width/2 + 300, 20, text = data.redScore, fill = data.colors["red"], font = data.fontTimer)
	canvas.create_text(data.width/2 - 300, 20, text = data.blueScore, fill = data.colors["blue"], font = data.fontTimer)

####################################
# single mode
####################################

def singleMousePressed(event, data):
	if data.turnActive and event.x > data.margin and event.x < data.margin + data.cellWidth*data.numCells:
		if event.y > data.margin and event. y < data.margin + data.cellHeight*data.numCells:
			row = (event.y - data.margin) // data.cellHeight
			col = (event.x - data.margin)// data.cellWidth
			clickedWord = data.gameMap[int(row)][int(col)]
			clickedWord.isClickedOn = True
		

def singleKeyPressed(event, data):
	#Scrolls screen around when arrow keys pressed
	pass


def singleTimerFired(data):
	if data.timerCalls % 10 == 0: #Every second
		data.time -= 1
	data.timerCalls += 1
	if data.time < 1:
		data.mode = "end"
	

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
						text = str(data.time), font=data.fontTimer)
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