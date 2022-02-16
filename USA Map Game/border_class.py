from turtle import RawTurtle


# set border dimensions
BORDER_HEIGHT = 500
BORDER_WIDTH = 800

# extend window from border for buffer
WINDOW_HEIGHT = BORDER_HEIGHT + 100
WINDOW_WIDTH = BORDER_WIDTH + 100

# specify canvas dimensions to accommodate scoreboard
CANVAS_HEIGHT = 500
CANVAS_WIDTH = 850

# specify ball/border/paddle width
PIXEL_WIDTH = 20
# divisor is to program that there for every object it's width is twice the pixel width
DIVISOR = 2

# specify border limits
UPPER_LIMIT = (BORDER_HEIGHT / DIVISOR) - PIXEL_WIDTH
LOWER_LIMIT = (-1 * (BORDER_HEIGHT / DIVISOR)) + PIXEL_WIDTH
LEFT_LIMIT = (-1 * (BORDER_WIDTH / DIVISOR)) + PIXEL_WIDTH
RIGHT_LIMIT = (BORDER_WIDTH / DIVISOR) - PIXEL_WIDTH

# arrange border corners
BORDER_COORDINATES = [(LEFT_LIMIT-20, LOWER_LIMIT-20),
                      (RIGHT_LIMIT+20, LOWER_LIMIT-20),
                      (RIGHT_LIMIT+20, UPPER_LIMIT+20),
                      (LEFT_LIMIT-20, UPPER_LIMIT+20)]




class Border(RawTurtle):
    def __init__(self, canv_obj):
        super().__init__(canvas=canv_obj, visible=False)
        self.ht()
        self.color("white")
        self.pencolor("black")
        self.pensize(5)
        self.penup()
        self.speed("fastest")
        self.upper_limit = UPPER_LIMIT
        self.southern_limit = LOWER_LIMIT
        self.left_limit = LEFT_LIMIT
        self.right_limit = RIGHT_LIMIT
        self.create_border()

    def create_border(self):
        for n in range(0, 4):
            self.goto(BORDER_COORDINATES[n])
            self.pendown()
        self.goto(BORDER_COORDINATES[0])