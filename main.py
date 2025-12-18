from cmu_graphics import *
import random
import math

Rect(0, 0, 400, 400, fill=rgb(15, 15, 20))

app.playerScore = 0
app.computerScore = 0
app.totalGames = 0 
app.lifetimeWins = 0
app.playerChoice = None
app.computerChoice = None
app.gameOver = False
app.isCounting = False
app.countdownValue = 3
app.timer = 0

choices = ['rock', 'paper', 'scissors']
accentColor = rgb(0, 200, 255)
winColor = rgb(50, 255, 150)
loseColor = rgb(255, 70, 100)
neutralColor = rgb(140, 140, 150)

def drawRockIcon(x, y, size, color):
    iconGroup = Group()
    iconGroup.add(Polygon(x, y-size*0.6, x+size*0.7, y-size*0.2, 
                          x+size*0.5, y+size*0.6, x-size*0.5, y+size*0.6,
                          x-size*0.7, y-size*0.2, fill=color))
    iconGroup.centerX, iconGroup.centerY = x, y
    return iconGroup

def drawPaperIcon(x, y, size, color):
    iconGroup = Group()
    iconGroup.add(Rect(x, y, size*1.1, size*1.4, fill=color, align='center'))
    iconGroup.centerX, iconGroup.centerY = x, y
    return iconGroup

def drawScissorsIcon(x, y, size, color):
    iconGroup = Group()
    iconGroup.add(Line(x-size*0.4, y-size*0.4, x+size*0.4, y+size*0.4, fill=color, lineWidth=4))
    iconGroup.add(Line(x-size*0.4, y+size*0.4, x+size*0.4, y-size*0.4, fill=color, lineWidth=4))
    iconGroup.centerX, iconGroup.centerY = x, y
    return iconGroup

instructionLabel = Label('SELECT WEAPON', 200, 300, fill=accentColor, size=12, font='monospace', bold=True)
resultText = Label('', 200, 160, fill='white', size=40, bold=True, font='monospace')
winRateLabel = Label('WIN RATE: 0%', 200, 70, fill=neutralColor, size=10, font='monospace')
snarkyLabel = Label('WAITING FOR INPUT...', 200, 45, fill=accentColor, size=11, font='monospace')

playerScoreLabel = Label('0', 100, 230, fill=accentColor, size=30, bold=True, font='monospace')
computerScoreLabel = Label('0', 300, 230, fill=loseColor, size=30, bold=True, font='monospace')
Label('YOU', 100, 100, fill=neutralColor, size=12, font='monospace')
Label('CPU', 300, 100, fill=neutralColor, size=12, font='monospace')

buttons = Group()
buttonList = [] 
btnChoices = ['rock', 'paper', 'scissors']
btnIcons = [drawRockIcon, drawPaperIcon, drawScissorsIcon]

for i in range(3):
    x = 80 + i * 120 
    b = Rect(x, 350, 90, 60, fill=rgb(25, 25, 35), border=rgb(60, 60, 70), borderWidth=1, align='center')
    icon = btnIcons[i](x, 350, 15, neutralColor)
    buttons.add(b, icon)
    buttonList.append(b)

restartBtn = Group(
    Rect(200, 265, 100, 25, fill=None, border=accentColor, align='center'),
    Label('RESET SCORE', 200, 265, fill='white', size=9, bold=True, font='monospace')
)
restartBtn.visible = False

playerIcon = Group()
computerIcon = Group()

def updateWinRate():
    if app.totalGames > 0:
        rate = (app.lifetimeWins / app.totalGames) * 100
        winRateLabel.value = f"LIFETIME WIN RATE: {rate:.1f}%"
        if rate > 60: snarkyLabel.value = "WOAH UR BETTER THAN AN AI!!!!"
        elif rate > 50: snarkyLabel.value = "NOT BAD, HUMAN."
        elif rate < 40: snarkyLabel.value = "MY GRANDMA PLAYS BETTER."
        elif rate == 30: snarkyLabel.value = "YOU fricking SUCK"
        else: snarkyLabel.value = "PERFECTLY AVERAGE. HOW BORING."

def resetButtonBorders():
    for item in buttons.children:
        if isinstance(item, Rect):
            item.border = rgb(60, 60, 70)

def showResult():
    app.computerChoice = random.choice(choices)
    pFunc = btnIcons[choices.index(app.playerChoice)]
    cFunc = btnIcons[choices.index(app.computerChoice)]
    playerIcon.add(pFunc(100, 160, 35, accentColor))
    computerIcon.add(cFunc(300, 160, 35, loseColor))

    if app.playerChoice == app.computerChoice:
        resultText.value, resultText.fill = "DRAW", neutralColor
        instructionLabel.value = "TIE! GO AGAIN"
    else:
        app.totalGames += 1
        if (app.playerChoice == 'rock' and app.computerChoice == 'scissors') or \
           (app.playerChoice == 'paper' and app.computerChoice == 'rock') or \
           (app.playerChoice == 'scissors' and app.computerChoice == 'paper'):
            resultText.value, resultText.fill = "WIN", winColor
            app.playerScore += 1
            app.lifetimeWins += 1
            playerScoreLabel.value = app.playerScore
        else:
            resultText.value, resultText.fill = "LOSE", loseColor
            app.computerScore += 1
            computerScoreLabel.value = app.computerScore
        
        updateWinRate()
        app.gameOver = True
        restartBtn.visible = True
        instructionLabel.visible = False

def onMousePress(x, y):
    if restartBtn.visible and restartBtn.hits(x, y):
        app.playerScore = app.computerScore = 0
        playerScoreLabel.value = computerScoreLabel.value = 0
        resetGame()
    elif not app.gameOver and not app.isCounting:
        for i, btn in enumerate(buttonList):
            if btn.hits(x, y):
                resetButtonBorders()
                btn.border = accentColor
                app.playerChoice = btnChoices[i]
                startCountdown()

def startCountdown():
    app.isCounting = True
    app.countdownValue = 3
    app.timer = 0
    playerIcon.clear()
    computerIcon.clear()
    resultText.value = "3"
    instructionLabel.visible = False

def resetGame():
    app.gameOver = False
    playerIcon.clear()
    computerIcon.clear()
    resetButtonBorders()
    resultText.value = ""
    instructionLabel.value = "CHOOSE YOUR WEAPON"
    restartBtn.visible = False
    instructionLabel.visible = True

def onStep():
    if app.isCounting:
        app.timer += 1
        if app.timer % 20 == 0:
            app.countdownValue -= 1
            if app.countdownValue > 0:
                resultText.value = str(app.countdownValue)
            elif app.countdownValue == 0:
                resultText.value = "GO!"
            else:
                app.isCounting = False
                showResult()

cmu_graphics.run()