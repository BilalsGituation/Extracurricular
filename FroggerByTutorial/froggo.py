import turtle
import math

'''
Context: I made Pong using @TokyoEdtech's tutorial on YouTube and am checking out
his other game tutorials


Day 1 finish commentary (03.05.2022):
revised: movement functions and keybinding, turtle window/mainloop,
learned: using images, class inheritance, pulling gifs from the pwd, new kind of collision
'''

# Window
wn = turtle.Screen()
wn.setup(600,800)
wn.cv._rootwindow.resizable(False,False)
wn.title("Just Frogging Away")
wn.bgcolor("black")
wn.tracer(0)

#register our shapes
# I would do this with all the shapes first? Maybe it makes tutorial narrative weird
wn.register_shape("frog.gif")
wn.register_shape("background.gif")
wn.register_shape("car_left.gif")
wn.register_shape("car_right.gif")
wn.register_shape("frog_home.gif")
wn.register_shape("frog_small.gif")
#wn.register_shape("goal.png") # guessed wrong
wn.register_shape("home.gif")
wn.register_shape("log_full.gif")
wn.register_shape("log_half.gif")
wn.register_shape("turtle_left.gif")
wn.register_shape("turtle_left_half.gif")
wn.register_shape("turtle_right.gif")
wn.register_shape("turtle_right_half.gif")
wn.register_shape("turtle_submerged.gif")


#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()


#Making classes
class Sprite():
    """docstring for Sprite."""

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y=y
        self.width=width
        self.height=height
        self.image=image

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def is_collision(self, other):
        x_collision=((math.fabs(self.x - other.x) *2) < (self.width + other.width))
        y_collision=((math.fabs(self.y - other.y) *2) < (self.height + other.height))
        return (x_collision and y_collision)


class Player(Sprite):

    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)

    def frog_up(self):
        self.y += 40
    def frog_left(self):
        self.x -= 40
    def frog_down(self):
        self.y -= 40
    def frog_right(self):
        self.x += 40


class Car(Sprite):

    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx

    def update(self):
        self.x += self.dx
        #Border checking
        if self.x < -400:
            self.x=400
        if self.x > 400:
            self.x=-400



#Making Objects
Player=Player(0,-300, 40, 40, "frog.gif")
Player.render(pen)

car_left = Car(0,-255,121,40,"car_left.gif", -0.15)
car_right = Car(0,255,121,40,"car_right.gif", 0.15)

# Key binds
wn.listen()
wn.onkeypress(Player.frog_up, "w")
wn.onkeypress(Player.frog_left, "a")
wn.onkeypress(Player.frog_down, "s")
wn.onkeypress(Player.frog_right, "d")
wn.onkeypress(Player.frog_up, "Up")
wn.onkeypress(Player.frog_left, "Left")
wn.onkeypress(Player.frog_down, "Down")
wn.onkeypress(Player.frog_right, "Right")

while True:
    #render
    Player.render(pen)
    car_left.render(pen)
    car_right.render(pen)

    # Update objects and Screen
    car_left.update()
    car_right.update()
    '''log_full.update()
    log_half.update()
    home.update()
    turtle_right.update()
    turtle_right_half.update()
    turtle_left.update()
    turtle_left_half.update()
    turtle_submerged.update()'''

    #Check for collisions
    if Player.is_collision(car_left):
        Player.x=0
        Player.y=-300

    if Player.is_collision(car_right):
        Player.x=0
        Player.y=-300


    wn.update()
    #clear frog
    pen.clear()


wn.mainloop()
