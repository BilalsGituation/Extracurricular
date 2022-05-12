import turtle
import math
import time
import random

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
# turns out the tutorial author made these himself using clipart in session 2
# I should try making some sprites on next project
shapes = ["frog.gif", "car_left.gif", "car_right.gif", "log_full.gif", "turtle_left.gif", "turtle_right.gif", "turtle_right_half.gif",
    "turtle_left_half.gif", "turtle_submerged.gif", "home.gif", "frog_home.gif", "frog_small.gif"]
for shape in shapes:
    wn.register_shape(shape)
'''
#wn.register_shape("goal.png") # guessed wrong
wn.register_shape("log_full.gif")
wn.register_shape("log_half.gif") # doesn't ever get used?
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
        self.dx = 0

    def frog_up(self):
        self.y += 40
    def frog_left(self):
        self.x -= 40
    def frog_down(self):
        self.y -= 40
    def frog_right(self):
        self.x += 40
    def update(self):
        self.x += self.dx
    # player is bordered in. see commits for more verbose explanation
        if Player.x < -300:
            Player.x = -300
        if Player.x > 300:
            Player.x = 300
        if Player.y < -380:
            Player.y = -380
        if Player.y > 380:
            Player.y = 380
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
            self.x=-400 # Yep, he just pastes a copy of this in while giving the tutorial


# Turts (turtles) is non-player object like logs, not cars, where collisions
# reset the frog
# EXCEPT the turtles (all? no, from the imageset?) sink when you stay on them
# for too long.. I think, based on there being a "turtle_submerged.gif" file in
# the GitHub repository accompanying the tutorial

class Turt(Sprite): # confusingly, this turtle means... turtles.. :|
# so we're going to call this turtle "turt" for clarity
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx
        self.state = "full" # half, submerged
        self.full_time = random.randint(8, 12)
        self.half_time = random.randint(4, 6)
        self.submerged_time = random.randint(4, 6)
        self.start_time = time.time()

    def update(self):
        self.x += self.dx
        #Border checking
        if self.x < -400:
            self.x=400
        if self.x > 400:
            self.x=-400
        # update img based on state
        if self.state == "full":
            if self.dx > 0:
                self.image = "turtle_right.gif"
            else:
                self.image = "turtle_left.gif"
        elif self.state == "half_up" or self.state == "half_down":
            if self.dx > 0:
                self.image = "turtle_right_half.gif"
            else:
                self.image = "turtle_left_half.gif"
        elif self.state == "submerged":
            self.image = "turtle_submerged.gif"
# Actually the home might more likely be another child of Sprite

# Timer stuff
        if self.state == "full" and time.time() - self.start_time > self.full_time:
            self.state = "half_down"
            self.start_time = time.time()
        elif self.state == "half_down" and time.time() - self.start_time > self.half_time:
            self.state = "submerged"
            self.start_time = time.time()
        elif self.state == "submerged" and time.time() - self.start_time > self.submerged_time:
            self.state = "half_up"
            self.start_time = time.time()
        elif self.state == "half_up" and time.time() - self.start_time > self.half_time:
            self.state = "full"
            self.start_time = time.time()

#Making Objects
Player=Player(0,-300, 40, 40, "frog.gif")
#Player.render(pen) #not sure why this was duplicated?

car_left = Car(0,-255,121,40,"car_left.gif", -0.15)
car_right = Car(0,-175,121,40,"car_right.gif", 0.15)
log_left = Log(0,-130,121,40,"log_full.gif", -0.25)
log_right = Log(0,-85,121,40,"log_full.gif", 0.25)
turt_left = Turt(0,-40,151,40,"turtle_left.gif", -0.2)
turt_right = Turt(0,15,151,40,"turtle_right.gif", 0.2)
log_left2 = Log(0,50,121,40,"log_left.gif", -0.2)
turt_left2 =  Turt(400,140,151,40,"turtle_left.gif", -0.3) # I have no idea why the frog stays on the other non-player non-car characters but this one is buggy
log_right2 = Log(0,185,121,40,"log_full.gif", 0.3)
log_right3 = Log(-400,95,121,40,"log_full.gif", 0.3)
log_left3 = Log(0,65,121,40,"log_full.gif", -0.35)

movements = [car_left, car_right, log_left, log_right, turt_left, turt_right, turt_left2, turt_left2, log_right2, log_left3, log_right3]
# Player is updated and rendered last
movements.append(Player)

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

    # Trying to be original and neater here, just leaving the mess for this commit at least, so it's not a copy-pasted version of the game
    #Player.render(pen) # he's right in the video that we will want the frog to be drawn on top of the log
    # update: that's great. since the loop goes fast enough in a collision with a car
    # update: I really did clean these up by guessing, not because I was eventually told to by the vid
    for object in movements:
        object.render(pen)
        object.update() # Update: my logs and cars were moving just fine now, the game ran



#
    Player.dx = 0
    for Sprite in movements:
        if Player.is_collision(Sprite):
            if isinstance(Sprite, Car):
                Player.x = 0
                Player.y = -300
                break
            elif isinstance(Sprite, Log):
                Player.dx = Sprite.dx
                break
            elif isinstance(Sprite, Turt):
                Player.dx = Sprite.dx
                break





#mainloop
    wn.update()
    #clear frog
    pen.clear()


wn.mainloop()
