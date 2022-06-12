import turtle # General Python packages required
import random
import platform
# Line 5 condition checks user system because sound must be accessed by cmd line
if platform.system() == "Linux":
    import os
    plat = "Linux"
elif platform.system() == "Darwin":
    import os # Linux and Mac
    plat = "Mac"
elif platform.system() == "Windows":
    import winsound # Windows
    plat = "Windows"

"""
CONTROLS:
Player 1: W = Up, S = Down. Player 2: Up Arrow = Up, Down Arrow = Down
Change colour of FG objects = F, Change colour of BG objects = B.

This game was made using a tutorial by @TokyoEdtech as part of a free YouTube series by freecodecamp.org.
The sounds required for this game are included in the GitHub repository.
This has only been tested on Linux.

Every effort should be made to make it clear what you need to change so that
this runs on your system, so let me know of any problems in the comments!
"""

# Cross-Platforming the Sounds - @BilalsGituation's idea to have system check be automated
def WallSound():
    if plat == "Linux":
        os.system("aplay 331381__qubodup__public-domain-jump-sound.wav&") # Linux
    elif plat == "Mac":
        os.system("afplay 331381__qubodup__public-domain-jump-sound.wav&") # Mac
    elif plat == "Windows":
        winsound.PlaySound("331381__qubodup__public-domain-jump-sound.wav", winsound.SND_ASYNC)
    else:
        turtle.bye()

def PadSound():
    if plat == "Linux":
        os.system("aplay 30252__voktebef__p.wav&") # Linux
    elif plat == "Mac":
        os.system("afplay 30252__voktebef__p.wav&") # Mac
    elif plat == "Windows":
        winsound.PlaySound("30252__voktebef__p.wav", winsound.SND_ASYNC)
    else:
        turtle.bye()

def GoalSound():
    if plat == "Linux":
        os.system("aplay 135512__chriddof__little-guy-sings.wav&") # Linux
    elif plat == "Mac":
        os.system("afplay 135512__chriddof__little-guy-sings.wav&") # Mac
    elif plat == "Windows":
        winsound.PlaySound("135512__chriddof__little-guy-sings.wav", winsound.SND_ASYNC)
    else:
        turtle.bye()

def ScoreFont():
    if plat == "Windows":
        pen.write(f"Player 1: {score_1}          Player 2: {score_2}", align="center", font=("Courier New", 24, "normal"))
    else:
        pen.write(f"Player 1: {score_1}          Player 2: {score_2}", align="center", font=("courier 10 pitch", 24, "normal"))


# Window
wn = turtle.Screen()
wn.title("Bill's Pongy Game") # It will be your game once you change stuff
wn.bgcolor("grey14")
wn.setup(width=800, height=600)
wn.tracer(0)


# Player left
leftpad = turtle.Turtle()
leftpad.speed(0)
leftpad.shape("square")
leftpad.shapesize(stretch_wid=5, stretch_len=1)
leftpad.color("grey76")
leftpad.penup()
leftpad.goto(-350,0)

# Player right
rightpad = turtle.Turtle()
rightpad.speed(0)
rightpad.shape("square")
rightpad.shapesize(stretch_wid=5, stretch_len=1)
rightpad.color("grey76")
rightpad.penup()
rightpad.goto(350,0)

# Non-Player Character (Ball)
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("grey76")
ball.penup()
ball.goto(0,0)
ball.dx = 0.3 #dx and dy values must be calibrated to one's own computer
ball.dy = 0.3

# Game scoring
score_1 = 0
score_2 = 0

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
ScoreFont()

# Paddle function -
def left_up():
    y= leftpad.ycor()
    y+=20
    leftpad.sety(y)

def left_down():
    y= leftpad.ycor()
    y-=20
    leftpad.sety(y)

def right_up():
    y= rightpad.ycor()
    y+=20
    rightpad.sety(y)

def right_down():
    y= rightpad.ycor()
    y-=20
    rightpad.sety(y)

# User can set colours

def RndFGColour():
    pen.clear()
    pen.color("#"+("%06x"%random.randint(0,16777215)))
    ScoreFont()
    ball.color("#"+("%06x"%random.randint(0,16777215)))
    leftpad.color("#"+("%06x"%random.randint(0,16777215)))
    rightpad.color("#"+("%06x"%random.randint(0,16777215)))

def RndBGColour():
    wn.bgcolor("#"+("%06x"%random.randint(0,16777215)))

# Keyboard binding
wn.listen()
wn.onkeypress(left_up, "w") # W key moves Player 1 up
wn.onkeypress(left_down, "s") # S key moves Player 1 down
wn.onkeypress(right_up, "Up") # Up key moves Player 2 up
wn.onkeypress(right_down, "Down") # Down key moves Player 2 down
wn.onkeypress(RndFGColour, "f") # F key changes colour of each foreground object to random
wn.onkeypress(RndBGColour, "b") # B key changes colour of background to random

# Main loop
while True:
    wn.update()
    # Move the Ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    # Set the play boundary
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy = 0 - ball.dy
        WallSound()

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        WallSound()

    # Goal Responses
    if ball.xcor() > 390:
        ball.goto(0,0)
        ball.dx = random.uniform(-0.4,-0.4) # these random floats for movement speed were not in the tutorial
        ball.dy = random.uniform(-0.4,0.4)
        score_1 += 1
        pen.clear()
        GoalSound()
        ScoreFont()

    if ball.xcor() < -390:
        ball.goto(0,0)
        ball.dx = random.uniform(-0.4,0.4)
        ball.dy = random.uniform(-0.4,0.4)
        score_2 += 1
        pen.clear()
        GoalSound()
        ScoreFont()

    # Collision responses between player character and non-player character
    if ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < rightpad.ycor() + 40 and ball.ycor() > rightpad.ycor() -40):
        ball.setx(340)
        ball.dx *= -1
        PadSound()

    if ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < leftpad.ycor() + 40 and ball.ycor() > leftpad.ycor() -40):
        ball.setx(-340)
        ball.dx *= -1
        PadSound()

    # Border the paddles in
    if leftpad.ycor() > 250:
        leftpad.sety(250)

    if leftpad.ycor() < -250:
        leftpad.sety(-250)

    if rightpad.ycor() > 250:
        rightpad.sety(250)

    if rightpad.ycor() < -250:
        rightpad.sety(-250)
