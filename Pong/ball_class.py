from turtle import Turtle
from border_class import UPPER_LIMIT, LOWER_LIMIT
from random import randint
BALL_PPF = 30
ADJUSTMENT = 4

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_coordinate = 0
        self.y_coordinate = 0
        self.x_movement = BALL_PPF
        self.y_movement = BALL_PPF

    def move(self):
        """detects if there is a wall bounce and changes movement accordingly, then moves"""
        self.is_there_wall_bounce()
        self.goto(self.xcor() + self.x_movement, self.ycor() + self.y_movement)

    def is_there_wall_bounce(self):
        """detects if wall bounce and if there is reverses y-coordinate movement"""
        if self.ycor() + 1 >= UPPER_LIMIT or self.ycor() - 1 <= LOWER_LIMIT:
            self.y_movement *= -1

    def paddle_bounce(self, paddle):
        """detects if there is a collision with the paddles, if so reverses x-cor movement and adjusts
        speed based on where the paddle was hit
        the farther from the center of the paddle the ball is hit, the faster the ball will go"""
        if self.ycor() > paddle.ycor() and self.y_movement < 0:
            self.y_movement *= -1
        elif self.ycor() < paddle.ycor() and self.y_movement > 0:
            self.y_movement *= -1

        if self.x_movement < 0:
            self.x_movement = BALL_PPF
        elif self.x_movement > 0:
            self.x_movement = -1 * BALL_PPF

        if self.distance(paddle) > ((paddle.height / 2) + paddle.width) - 35:
            self.x_movement = self.x_movement * 2
        elif self.distance(paddle) > ((paddle.height / 2) + paddle.width) - 5:
            self.x_movement = self.x_movement * 3.5
        elif self.distance(paddle) > ((paddle.height / 2) + paddle.width) - 10:
            self.x_movement = self.x_movement * 3
        elif self.distance(paddle) > ((paddle.height / 2) + paddle.width) - 15:
            self.x_movement = self.x_movement * 2.75




