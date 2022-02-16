from turtle import Turtle
from border_class import LOWER_LIMIT, UPPER_LIMIT, LEFT_LIMIT, RIGHT_LIMIT

# initialize moving speed, finish line location, and turtle size
MOVING_VALUE = 10
FINISH_LINE = UPPER_LIMIT - 20
PLAYER_HEIGHT = 20

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.speed("fastest")
        self.shape("turtle")
        self.color("green")
        self.penup()
        self.goto(0, LOWER_LIMIT)
        self.st()
        self.setheading(90)

    def refresh(self):
        """bring turtle to starting position"""
        self.goto(0, LOWER_LIMIT)
        self.st()
        self.setheading(90)

    def move_up(self):
        """move turtle up"""
        self.setheading(90)
        self.forward(MOVING_VALUE)

    def move_down(self):
        """move turtle down"""
        if abs(LOWER_LIMIT) - abs(self.ycor()) > 10:
            self.setheading(270)
            self.forward(MOVING_VALUE)

    def move_left(self):
        """move turtle left"""
        if LEFT_LIMIT - self.xcor() < -10:
            self.setheading(180)
            self.forward(MOVING_VALUE)

    def move_right(self):
        """move turtle right"""
        if RIGHT_LIMIT - self.xcor() > 10:
            self.setheading(0)
            self.forward(MOVING_VALUE)