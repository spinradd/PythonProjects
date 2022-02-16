from turtle import Turtle, Screen
import random


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.color("cyan2")
        self.shapesize(stretch_len=.5, stretch_wid=.5)
        self.speed("fastest")
        self.goto(random.randrange(-280, 280), random.randrange(-180, 180))

    def move_food(self, snake_obj):
        """when food is eaten put the food in a random location. If food spawns within snake, respawn"""
        valid_spot = False
        while not valid_spot:
            x_coordinate = random.randrange(-280, 280)
            y_coordinate = random.randrange(-180, 180)
            for segment in snake_obj:
                if segment.distance(self) >= 40:
                    self.move_food
                    valid_spot = True
        self.goto(x_coordinate, y_coordinate)

    def delete_food(self):
        """deletes food from screen"""
        self.reset()

    def refresh(self):
        """remakes food at beginning of new game"""
        self.penup()
        self.shape("circle")
        self.color("cyan2")
        self.shapesize(stretch_len=.5, stretch_wid=.5)
        self.speed("fastest")
        self.goto(random.randrange(-280, 280), random.randrange(-180, 180))





