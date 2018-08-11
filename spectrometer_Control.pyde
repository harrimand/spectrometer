
newscreen = True
WvLen = 550 # Wavelength Set Value
Wpoint = 0  # Triangular Pointer for Wavelength Setting
Dpoint = 0  # Triangular Pointer to erase previous Wavelength Setting
preX = 0 # Mouse X Previous Value

def setup():
    global Wpoint, Dpoint, preX
    size(800, 400)
    background(0)
    stroke(255)
    strokeWeight(4)
    line(100, 300, 700, 300)
    preX = width/2
    Wpoint = mkPointer(color(0,255,0)) # Make Wavelength Set Pointer
    Dpoint = mkDPointer(color(0, 0, 0)) # Make Black Wavelength Set Pointer to erase Wavelength Setting

def draw():
    global newscreen
    if newscreen: # If true, update screen
        drawscrn()
        newscreen = False

def drawscrn(): 
    background(0)
    scrtxt = "Information Goes Here"
    textAlign(CENTER)
    textSize(36)
    text(scrtxt, width/2, height/2)
    stroke(255)
    strokeWeight(4)
    line(100, 300, width-100, 300)


def mouseClicked():
    global Wpoint, Dpoint, preX
    X = mouseX
    Y = mouseY
    if X > 100 and X < width-100 and Y > 275 and Y < 325:
        # stroke(255, 0, 0)
        # strokeWeight(2)
        # line(X, 275, X, 325)
        shape(Dpoint, preX-16, 267) # Erase previous set point
        shape(Wpoint, X-15, 268)    # Draw new set point
        preX = X

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
    
def mkDPointer(col = color(0, 0, 0)):
    # Create Triangular marker to delete previous Wavelength Set Point
    DP = createShape()
    DP.beginShape()
    DP.fill(col)
    DP.noStroke()
    DP.vertex(0, 0)
    DP.vertex(32, 0)
    DP.vertex(16, 32)
    DP.endShape(CLOSE)
    return DP


















    
    
    
    
    
    
    
    
    


