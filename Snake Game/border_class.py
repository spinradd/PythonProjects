from turtle import Turtle

# set limits of game screen
UPPER_LIMIT = 190
SOUTHERN_LIMIT = -190
LEFT_LIMIT = -290
RIGHT_LIMIT = 290
BORDER_COORDINATES = [(LEFT_LIMIT, SOUTHERN_LIMIT),
                      (RIGHT_LIMIT, SOUTHERN_LIMIT),
                      (RIGHT_LIMIT, UPPER_LIMIT),
                      (LEFT_LIMIT, UPPER_LIMIT)]

class Border(Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.color("white")
        self.pencolor("white")
        self.pensize(5)
        self.penup()
        self.speed("fastest")
        self.upper_limit = UPPER_LIMIT
        self.southern_limit = SOUTHERN_LIMIT
        self.left_limit = LEFT_LIMIT
        self.right_limit = RIGHT_LIMIT
        self.create_border()

    def create_border(self):
        """creates border for game screen"""
        for n in range(0, 4):
            self.goto(BORDER_COORDINATES[n])
            self.pendown()
        self.goto(BORDER_COORDINATES[0])

    def is_border_breached(self, turtle_head_obj):
        """return true when snake head comes within pixel threshold of border"""
        if (turtle_head_obj.xcor() <= self.left_limit or
                turtle_head_obj.xcor() >= self.right_limit):
            return True
        elif (turtle_head_obj.ycor() >= self.upper_limit or
              turtle_head_obj.ycor() <= self.southern_limit):
            return True
        else:
            return False

