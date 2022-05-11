import turtle
import math

'''
Context: I made Pong using @TokyoEdtech's tutorial on YouTube and am checking out
his other game tutorials. Found livestream tutorial playlist where he makes Frogger

Tutorial:
YouTube: https://www.youtube.com/watch?v=CDM4U5A7BX8&list=PLlEgNdBJEO-lR6IChlbqU1E00vpN3GBM6

Imageset or script if that's how you learn:
GitHub: https://github.com/wynand1004/Projects/tree/master/Frogger


Day 1 finish commentary (03.05.2022):
revised: movement functions and keybinding, turtle window/mainloop,
learned: using images, class inheritance, pulling gifs from the pwd, new kind of collision
Morning after: car should be down by where road will be, like in video. Made placeholders
for other aspects of game to get thinking about concepts

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
# 11.05.2022 (May ofc) I went on the github script of this game and had a facepalm moment when I saw this was done by a "for" loop. That's why I practice!
# Of course I just copy-pasted the list of shapes from the GitHub, I had already individually copied them in

# register shapes in wn
shapes = ["frog.gif", "car_left.gif", "car_right.gif", "log_full.gif", "turtle_left.gif", "turtle_right.gif", "turtle_right_half.gif",
    "turtle_left_half.gif", "turtle_submerged.gif", "home.gif", "frog_home.gif", "frog_small.gif"]
for shape in shapes:
    wn.register_shape(shape)
'''
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
'''

#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()


#Making classes (removed docstring, won't pretend I remember what it does)
class Sprite():
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
# somehow the player needs to get to the goal. Either function here or new child



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

# Morning after Day 1:
# Saving myself typing along with the tutorial:
# Predicting the other classes

# Log is a platform to stand on in river area
# so I will want to somehow invert the collision function so floor sends you back
# and log allows continuation

class Log(Sprite):

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

# Turts (turtles) is non-player object like logs, not cars, where collisions
# reset the frog
# EXCEPT the turtles (all? no, from the imageset?) sink when you stay on them
# for too long.. I think, based on there being a "turtle_submerged.gif" file in
# the GitHub repository accompanying the tutorial

class Turts(Sprite):

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

# Actually the home might more likely be another child of Sprite



#Making Objects
Player=Player(0,-300, 40, 40, "frog.gif")
Player.render(pen)

car_left = Car(0,-255,121,40,"car_left.gif", -0.15)
car_right = Car(0,255,121,40,"car_right.gif", 0.15)

# Space to Make logs



# Space to Make turts

# Make home



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

# mainloop properties
while True:
    #render
    # Placeholder/guess: "for shape in shapes: shape.render(pen)"
    Player.render(pen)
    car_left.render(pen)
    car_right.render(pen)

    # Update objects and Screen
    # Placeholder/guess: "for sprite in sprites: sprite.update()"
    # Maybe I can design it that way, maybe it's inefficient. Maybe it's better as a sprite function, as it is looking like on the GitHub for the tutorial
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


    #Call functions you built in
    #Check for collisions
    if Player.is_collision(car_left):
        Player.x=0
        Player.y=-300

    if Player.is_collision(car_right):
        Player.x=0
        Player.y=-300

    # Behaviour of objects that save the frog from drowning
    # and the function of the frog getting in the goal



#mainloop
    wn.update()
    #clear frog
    pen.clear()


wn.mainloop()
