'''
# Pseudocode:

import arcade, random and timeit

set up your screen

set width and height for rectangle? (didn't get called again and worked with comment-out)

define parent class shape
	init with static and dynamic spatial attribs
	move with changes to dynamic attribs per frame (stuff like x+=dx)

define specific shapes using arcade draw_shape_state() or Var.draw()

start MyGame class (child of arcade.Window class) for render loop
	inits with placeholder variables for statistics tdw program running

	setup function starts a shape list with length set by user at beginning
		for each shape, set instance attributes
		shape randomly chosen and attribs go in

	update function uses timeit to factor processing time into movement of shapes

	draw function renders the scene (screen then fg objects then timings)

call MyGame	in main function

run main()

'''
