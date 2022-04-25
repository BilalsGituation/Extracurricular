import turtle

# Window
wn = turtle.Screen()
wn.title("Bill's Pongy Game")
wn.bgcolor("grey14")
wn.setup(width=800, height=600)
wn.tracer(0)

# Player left - left paddle
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

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("grey76")
ball.penup()
ball.goto(0,0)
ball.dx = 0.2
ball.dy = -0.2


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

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
"""
    if ball.xcor() < 390:
        ball.setx(390)
        ball.dx *= -1

    if ball.xcor() < -390:
        ball.setx(-290)
        ball.dx *= -1"""
