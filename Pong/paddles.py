from turtle import Turtle
from border_class import UPPER_LIMIT, LOWER_LIMIT, LEFT_LIMIT, RIGHT_LIMIT

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        # self.ht()
        self.penup()
        self.speed("fastest")
        self.color("cyan2")
        self.shape("square")
        self.turtlesize(stretch_wid=5, stretch_len=1)
        self.body = []
        self.score = 0
        self.player = 0
        self.edge_limit = 0
        self.height = PADDLE_HEIGHT
        self.width = PADDLE_WIDTH

    def create_left(self): #"head" of bar will be lowest square
        """place left paddle on left side"""
        self.edge_limit = LEFT_LIMIT
        self.player = 1
        self.goto(self.edge_limit, 0)


    def create_right(self): #"head" of bar will be lowest square
        """place right paddle on right side"""
        self.edge_limit = RIGHT_LIMIT
        self.player = 2
        self.goto(self.edge_limit, 0)

    def move_up(self):
        """mode paddle up one square or 20 pixels"""
        if self.ycor() + 50 < UPPER_LIMIT:
            self.setposition(self.xcor(), self.ycor() + 20)

    def move_down(self):
        """mode paddle down one square or 20 pixels"""
        if self.ycor() - 50 > LOWER_LIMIT:
            self.setposition(self.xcor(), self.ycor() - 20)
