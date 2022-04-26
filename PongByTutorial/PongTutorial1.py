import turtle
import random
import platform
import os # Linux and Mac
#import winsound # Windows - Comment out or install yourself if not applicable
# So.. this game can either be compatible for Mac&Linux OR Windows at present.

"""
This game was made using a tutorial by @TokyoEdtech as part of a free YouTube series by freecodecamp.org.
The sounds required for this game are included in the GitHub repository.
This has only been tested on Linux.

Every effort should be made to make it clear what you need to change so that this runs on your system, so let me know of any problems in the comments!
"""

# Cross-Platforming the Sounds
def WallSound():
    if platform.system() == "Linux":
        os.system("aplay 331381__qubodup__public-domain-jump-sound.wav&") # Linux
    elif platform.system() == "Darwin":
        os.system("afplay 331381__qubodup__public-domain-jump-sound.wav&") # Mac
    elif platform.system() == "Windows":
        winsound.PlaySound("31381__qubodup__public-domain-jump-sound.wav", winsound.SND_ASYNC)
    else:
        turtle.bye()

def PadSound():
    if platform.system() == "Linux":
        os.system("aplay 30252__voktebef__p.wav&") # Linux
    elif platform.system() == "Darwin":
        os.system("afplay 30252__voktebef__p.wav&") # Mac
    elif platform.system() == "Windows":
        winsound.PlaySound("30252__voktebef__p.wav", winsound.SND_ASYNC)
    else:
        turtle.bye()

def GoalSound():
    if platform.system() == "Linux":
        os.system("aplay 135512__chriddof__little-guy-sings.wav&") # Linux
    elif platform.system() == "Darwin":
        os.system("afplay 135512__chriddof__little-guy-sings.wav&") # Mac
    elif platform.system() == "Windows":
        winsound.PlaySound("afplay 135512__chriddof__little-guy-sings.wav", winsound.SND_ASYNC)
    else:
        turtle.bye()

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
ball.dx = 0.2 #dx and dy values must be calibrated to one's own computer
ball.dy = 0.2

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
pen.write("Player 1: 0          Player 2: 0".format(score_1, score_2), align="center", font=("courier 10 pitch", 24, "normal"))

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

# Keyboard binding
wn.listen()
wn.onkeypress(left_up, "w")
wn.onkeypress(left_down, "s")
wn.onkeypress(right_up, "Up")
wn.onkeypress(right_down, "Down")

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
        GoalSound()
        pen.clear()
        pen.write("Player 1: {}          Player 2: {}".format(score_1, score_2), align="center", font=("courier 10 pitch", 24, "normal"))

    if ball.xcor() < -390:
        ball.goto(0,0)
        ball.dx = random.uniform(-0.4,0.4)
        ball.dy = random.uniform(-0.4,0.4)
        score_2 += 1
        GoalSound()
        pen.clear()
        pen.write("Player 1: {}          Player 2: {}".format(score_1, score_2), align="center", font=("courier 10 pitch", 24, "normal"))

    # Collision responses between player character and non-player character
    if ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < rightpad.ycor() + 40 and ball.ycor() > rightpad.ycor() -40):
        ball.setx(340)
        ball.dx *= -1
        PadSound()

    if ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < leftpad.ycor() + 40 and ball.ycor() > leftpad.ycor() -40):
        ball.setx(-340)
        ball.dx *= -1
        PadSound()
