# Photospectromer Controller
# Author: Darrell Harriman
newscreen = True
WvLen = 550 # Wavelength Set Value
Wpoint = 0  # Triangular Pointer for Wavelength Setting
Dpoint = 0  # Triangular Pointer to erase previous Wavelength Setting
marks = 0
WpX = 400   #Initial Wavelength Pointer X value
preX = 0 # Mouse X Previous Value
BG = color(0, 64, 128) # Background Color (R, G, B)

def setup():
    global Wpoint, Dpoint, preX, marks
    size(800, 400)
    background(BG)
    stroke(255)  # Make White Line
    strokeWeight(4) # Set line thickness
    line(100, 300, 700, 300) # line from (x1, y1, x2, y2)
    preX = width/2 # Initializing preX.  Value irrelevant
    Wpoint = mkPointer(color(0,255,0)) # Make Wavelength Set Pointer
    Dpoint = mkDPointer() # Make Black Wavelength Set Pointer to erase Wavelength Setting
    marks = mkScaleTicks()

def draw():
    global newscreen
    if newscreen: # If true, update screen
        drawscrn()
        newscreen = False

def drawscrn():
    # Draw screen
    global WvLen, BG, WpX
    background(BG)
    headTxt = "Spectrophotometer Control"
    scrtxt = "Set Wavelength: "
    setStr = str(WvLen)
    textAlign(CENTER)
    textSize(36)
    text(headTxt, width/2, 50)
    text(scrtxt, width/2 - 80, height/2)
    
    noStroke()
    fill(BG)
    rectMode(CENTER)
    rect(width/2 + 100, height/2-15, 100, 50)
    
    fill(255)
    text(setStr, width/2 + 100, height/2)
    
    stroke(255)
    fill(255)
    strokeWeight(4)
    line(100, 300, width-100, 300)
    shape(Wpoint, WpX-15, 268)
    shape(marks, 100, 300)
    ticklabels(100, 325)


def mouseClicked():
    global Wpoint, Dpoint, preX, WvLen
    X = mouseX
    Y = mouseY
    if X > 100 and X < width-100 and Y > 275 and Y < 325:
        # stroke(255, 0, 0)
        # strokeWeight(2)
        # line(X, 275, X, 325)
        shape(Dpoint, preX-16, 267) # Erase previous set point
        shape(Wpoint, X-15, 268)    # Draw new set point
        WpX = X
        WvLen = int(map(X, 100, width-100, 400, 700)) 
        preX = X
        noStroke()
        fill(BG)
        rectMode(CENTER)
        rect(width/2 + 100, height/2-15, 100, 50) # Erase previous wavelength
        fill(255)
        textSize(36)
        setStr = str(WvLen)
        text(setStr, width/2 + 100, height/2)


def mkPointer( col ):
    # Create Triangular marker for Wavelength Set Point
    WP = createShape()
    WP.beginShape()
    WP.fill(col)
    WP.noStroke()
    WP.vertex(0, 0)
    WP.vertex(30, 0)
    WP.vertex(15, 30)
    WP.endShape(CLOSE)
    return WP
    
def mkDPointer():
    # Create Triangular marker to delete previous Wavelength Set Point
    global BG
    DP = createShape()
    DP.beginShape()
    DP.fill(BG)
    DP.noStroke()
    DP.vertex(0, 0)
    DP.vertex(32, 0)
    DP.vertex(16, 32)
    DP.endShape(CLOSE)
    return DP

def mkScaleTicks():
    global marks
    stroke(255,0, 255)
    marks = createShape()
    marks.beginShape(LINES)
    for m in range(0, width-200+1, int((width-200)/30)):
        marks.vertex(m, 4)
        marks.vertex(m, 10)
    text("400", 100, 20)
    marks.endShape()
    
    return marks

def ticklabels(x, y):
    wL = 400
    stroke(255)
    textSize(10)
    textAlign(CENTER)
    for t in range(0, width-200+1, int((width-200)/6)):
        text(str(wL), t + x, y)
        wL = wL + 50        
