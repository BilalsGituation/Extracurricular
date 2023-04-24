import arcade

SCREEN_WIDTH= 800
SCREEN_HEIGHT = 600

class Element:
	def __init__(self,x,y,width,height,colour,dx,dy,d_angle):
		self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.dx = dx
        self.dy = dy
        self.d_angle = d_angle
        self.shape_list = None
    
    def move(self):
    	self.x += self.dx
        self.y += self.dy
        if self.x < 0 and self.delta_x < 0:
            self.delta_x *= -1
        if self.y < 0 and self.delta_y < 0:
            self.delta_y *= -1
        if self.x > SCREEN_WIDTH and self.delta_x > 0:
            self.delta_x *= -1
        if self.y > SCREEN_HEIGHT and self.delta_y > 0:
            self.delta_y *= -1

    def draw(self):
        self.shape_list.center_x = self.x
        self.shape_list.center_y = self.y
        # self.shape_list.angle = self.angle
        self.shape_list.draw()

class Sun(Element):
	def __init__(self, x, y, width, height, angle, dx, dy,
                 d_angle, colour):

        super().__init__(x, y, width, height, angle, delta_x, delta_y,
                         delta_angle, colour)
        self.width = self.height
        shape = arcade.create_circle_filled(0, 0,
                                             self.width, self.height,
                                             self.colour, self.angle)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)

class MyGame(arcade.Window):
	def __init__(self):
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

	def setup(self):
		self.shape_list = []
		x = random.randrange(0, SCREEN_WIDTH)
        y = random.randrange(0, SCREEN_HEIGHT)
        width = 68
        height = width
        colour = arcade.color.YELLOW
        d_x = random.randrange(-3, 4)
        d_y = random.randrange(-3, 4)
        d_angle = random.randrange(-3, 4)

        
        arcade.draw_ellipse_filled(x, y, width, arcade.color.YELLOW)
		draw_background()

	def on_update(self,time):

	def on_draw(self):
		arcade.start_render()

        for shape in self.shape_list:
            shape.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()