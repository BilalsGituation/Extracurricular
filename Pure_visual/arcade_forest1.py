"""
Example "Arcade" library code.

This example shows how to use functions and loops to draw a scene.
It does not assume that the programmer knows how to use classes yet.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.drawing_with_loops
"""

#Developed using:
# https://api.arcade.academy/en/2.6.1/examples/drawing_with_loops.html#drawing-with-loops
# as jump-off point. You can see what existed in the template already.

# Library imports
import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Drawing With Loops Example"


def draw_background():
    """
    This function draws the background. Specifically, the sky and ground. (old, describes original)
    """
    # Draw the sky in the top two-thirds
    arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3,
                                 SCREEN_WIDTH - 1, SCREEN_HEIGHT * 2 / 3,
                                 (random.randint(55,200),random.randint(156,232),random.randint(190,230)))

# Give the sky a nice gradient (Challenge)
    color1 = (222, 190, 164,155)
    color2 = (222, 190, 164, 0)
    points = (0, SCREEN_WIDTH / 2), (SCREEN_WIDTH, 100), (SCREEN_WIDTH, 800), (0, 800)
    colors = (color2, color1, color1, color2)
    grad = arcade.create_rectangle_filled_with_colors(points, colors)
    grad.draw()

    color1 = (222, 190, 164,155)
    color2 = (222, 190, 164, 0)
    points = (SCREEN_WIDTH / 2,50), (500, 130), (SCREEN_WIDTH/(2/3), 800), (20, 450)
    colors = (color1,color2, color1, color2)
    grad = arcade.create_rectangle_filled_with_colors(points, colors)
    grad.draw()

    # Draw the ground in the bottom third
    arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6,
                                 SCREEN_WIDTH - 1, SCREEN_HEIGHT / 2.3 ,
                                 (32, 105, 59))


def draw_sun(x=SCREEN_WIDTH-680,y=SCREEN_HEIGHT-120):
    x,y = random.randint(0,SCREEN_WIDTH-550),random.randint(SCREEN_HEIGHT-220,SCREEN_HEIGHT-50)
    #arcade.draw_circle_filled(x, y, 68, arcade.color.YELLOW)
    # If sun x value too high, its y value not too low
    if x > SCREEN_WIDTH-600:
        y= random.randint(SCREEN_HEIGHT-140,SCREEN_HEIGHT-50)
    # If sun y too high, get normal mid-daytime colours, 
    # remove inappropriate "rays of light", using overwriting rectangle  
    if y >SCREEN_HEIGHT- 100:
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3,
                                 SCREEN_WIDTH - 1, SCREEN_HEIGHT * 2 / 3,
                                 (random.randint(55,156),
                                    random.randint(200,232),
                                    random.randint(220,255)))
        arcade.draw_circle_filled(x, y, 68, arcade.color.YELLOW)
    else:
        arcade.draw_circle_filled(x, y, 68, arcade.color.YELLOW)

# Uses RNGs for type, positioning, relative size and colour
# (Uncomment the text in, to get the clouds labelled, for modification
# Turn different components contrasting colour if you have trouble
# finding them)
def draw_cloud(x,y):
    seed=random.randint(0,3)

    def cloud_1():
        size=random.randint(24,39)
        r=random.randint(220,230)
        g=random.randint(220,230)
        b=random.randint(220,235)
        arcade.draw_circle_filled(x-size*.1, y, size, (r,g,b))
        arcade.draw_circle_filled(x+size*.7, y, size*(2/3), (r,g,b))
        arcade.draw_ellipse_filled(x+size*1.25, y-(0.25*size),size*1.7, size*1.1, (r,g,b))
        arcade.draw_ellipse_filled(x-(size/3),y-((2*size)/3),size*1.8,size+1,(r,g,b))
        arcade.draw_ellipse_filled(x+(size/7),y-(size/2.25),size*3,size+1,(r,g,b))
        #arcade.draw_text("1", x, y, arcade.color.BLACK, 12)

    def cloud_2():

        size=random.randint(18,28)
        r=random.randint(220,230)
        g=random.randint(220,235)
        b=random.randint(220,240)
        arcade.draw_circle_filled(x+2, y, size, (r,g,b))
        arcade.draw_circle_filled(x+size*1.1, y-(size/4), size/2, (r,g,b))
        arcade.draw_ellipse_filled(x,y-2,size*1.8,size,(r,g,b))
        arcade.draw_ellipse_filled(x+6,y-((2*size)/3),size*1.8,size+1,(r,g,b))
        arcade.draw_ellipse_filled(x-2.2,y-(size/2),size*3,size+1,(r,g,b))
        #arcade.draw_text("2", x, y, arcade.color.BLACK, 12)

    def cloud_3():
        size=random.randint(8,19)
        r=random.randint(220,245)
        g=random.randint(220,235)
        b=random.randint(220,240)
        arcade.draw_circle_filled(x-1, y, size, (r,g,b))
        #arcade.draw_text("3", x, y, arcade.color.BLACK, 12)

        arcade.draw_circle_filled(x+size, y+(size/2.5), size*0.6, (r,g,b))
        arcade.draw_circle_filled(x+(size*1.5), y+(size/4), size*0.87, (r,g,b))
        arcade.draw_ellipse_filled(x,y-2,size*1.3,size,(r,g,b))
        arcade.draw_ellipse_filled(x-6,y-2,size*2.7,size+1,(r,g,b))
        arcade.draw_ellipse_filled(x+2,y-6,size*6,size+1,(r,g,b))
    
    if seed == 0:
        cloud_1()
    elif seed == 1:
        cloud_2()
    elif seed == 2:
        cloud_3()
    else:
        cloud_1()



def draw_bird(x, y):
    """
    Draw a bird using a couple arcs.
    """
    arcade.draw_arc_outline(x, y, 20, 20, arcade.color.BLACK, 0, 90)
    arcade.draw_arc_outline(x+20, y, 20, 20, arcade.color.BLACK, 90, 180)

# Uses RNGs for type and relative size. 
# For loop in main() uses RNGs for positioning
def draw_pine_tree(center_x, center_y):
    """
    This function draws a pine tree at the specified location. (nope, updated this out)

    Args:
      :center_x: x position of the tree center.
      :center_y: y position of the tree trunk center.
    """
    #Challenge: crude variation of trees
    seed = random.randint(0,12)
    def tree_1():
        # Draw the trunkcenter_x
        arcade.draw_rectangle_filled(center_x, center_y+random.randint(7,12), 20, 40,
                                     arcade.color.DARK_BROWN)

        tree_bottom_y = center_y + 20

        # Draw the triangle on top of the trunk
        center_x_adj = random.randint(45,50)
        point_list = ((center_x - center_x_adj, tree_bottom_y),
                      (center_x, tree_bottom_y + random.randint(70,100)),
                      (center_x + center_x_adj, tree_bottom_y))

        arcade.draw_polygon_filled(point_list, (39, 82, 57))
        arcade.draw_polygon_outline(point_list, (0,0,0,40),1)

    def tree_2():
        # Draw the trunkcenter_x
        arcade.draw_rectangle_filled(center_x, center_y+random.randint(-8,5), 25, 50,
                                     (133, 87, 50))

        tree_bottom_y = center_y + 20

        # Draw the triangle on top of the trunk
        center_x_adj = random.randint(35,40)
        y_adj = random.randint(15,25)
        point_list = ((center_x - center_x_adj, tree_bottom_y-y_adj),
                      (center_x, tree_bottom_y + random.randint(70,120)),
                      (center_x + center_x_adj, tree_bottom_y-y_adj))

        arcade.draw_polygon_filled(point_list, (88, 191, 82))
        arcade.draw_polygon_outline(point_list, (0,0,0,40),1)

    def tree_3():
        # Draw the trunkcenter_x
        arcade.draw_rectangle_filled(center_x, center_y, 10, 40,
                                     (135, 41, 34))

        tree_bottom_y = center_y + 20

        # Draw the triangle on top of the trunk
        center_x_adj = random.randint(35,50)
        y_adj = random.randint(-20,0)
        point_list = ((center_x - center_x_adj, tree_bottom_y+y_adj),
                      (center_x, tree_bottom_y + random.randint(80,110)),
                      (center_x + center_x_adj, tree_bottom_y+y_adj))

        arcade.draw_polygon_filled(point_list, (84, 115, 77))
        arcade.draw_polygon_outline(point_list, (0,0,0,40),1)

    def tree_4():
        # Draw the trunkcenter_x
        arcade.draw_rectangle_filled(center_x, center_y+random.randint(7,12), 20, 40,
                                     arcade.color.DARK_BROWN)

        tree_bottom_y = center_y + 20

        # Draw the triangle on top of the trunk
        center_x_adj = random.randint(45,50)
        point_list = ((center_x - center_x_adj, tree_bottom_y),
                      (center_x, tree_bottom_y + random.randint(70,100)),
                      (center_x + center_x_adj, tree_bottom_y))

        arcade.draw_polygon_filled(point_list, (10, 51, 27))
        arcade.draw_polygon_outline(point_list, (0,0,0,40),1)


# Tree type likelihood is 2,3or5/13
    if seed == 0 or seed == 7 or seed == 9:
        tree_1()
    elif seed ==1 or seed ==3:
        tree_2()
    elif seed ==2 or seed == 5 or seed == 4 or seed ==11 or seed ==12:
        tree_3()
    elif seed == 6 or seed ==8 or seed == 10:
        tree_4()
    # edit seed range and you can get the for loop to also deposit spaces
    else:
        pass





def main():
    """
    This is the main program.
    """

    # Open the window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # Start the render process. This must be done before any drawing commands.
    arcade.start_render()

    # Call our drawing functions.
    draw_background()
    draw_sun()
    for cloud_count in range(1,random.randint(2,40)):
        draw_cloud(random.randint(0,SCREEN_WIDTH),random.randint(SCREEN_HEIGHT-200,SCREEN_HEIGHT-50))
    # Loop to draw ten birds in random locations.
    for bird_count in range(10):
        # Any random x from 0 to the width of the screen
        x = random.randrange(0, SCREEN_WIDTH)

        # Any random y from in the top 2/3 of the screen.
        # No birds on the ground.
        y = random.randrange(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 20)

        # Draw the bird.
        draw_bird(x, y)

    # Draw the top row of trees
    for x in range(45, SCREEN_WIDTH, 60):
        draw_pine_tree((x+random.choice([-(x*2),-(x*2),-(x/2),-(x*1.8),0,0,0,0,0,0,0,0,0,0])), (random.randint((SCREEN_HEIGHT / 3)-10,(SCREEN_HEIGHT/3)+10)))

    for x in range(50, SCREEN_WIDTH, 70):
        draw_pine_tree((x+random.choice([-(x*2),-(x*2),(x*-2),(x*-2),0,0,10,0,0,0,0,10])), (random.randint((SCREEN_HEIGHT / 3),(SCREEN_HEIGHT/3)+10)-30))

    for x in range(50, SCREEN_WIDTH, 70):
        draw_pine_tree((x+random.choice([-(x*2),-(x*2),(x*-2),(x*-2),0,0,10,0,0,0,0,10])), (random.randint((SCREEN_HEIGHT / 3)-50,(SCREEN_HEIGHT/3))-80))

    # Draw the bottom row of trees
    for x in range(65, SCREEN_WIDTH, 50):
        draw_pine_tree((x+random.choice([-(x*2),-(x*2),0,0,0,0,0,0,0,0,0,0,0,0,0,0,x])), (random.randint((SCREEN_HEIGHT / 3)-150,(SCREEN_HEIGHT/3)-50) - 70))

    # Finish the render.
    # Nothing will be drawn without this.
    # Must happen after all draw commands
    arcade.finish_render()

    # Keep the window up until someone closes it.
    arcade.run()


if __name__ == "__main__":
    main()