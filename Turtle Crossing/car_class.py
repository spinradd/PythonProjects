from turtle import Turtle
from random import randint
from border_class import LOWER_LIMIT, UPPER_LIMIT, RIGHT_LIMIT

# randomize speeds for cars
SPEEDS = [n for n in range(0, 10)]

# initialize car size and movement
STARTING_MOVE_DIST = 5
CAR_LENGTH = 40
CAR_HEIGHT = 20
MOVING_VALUE = 10

class Fleet():
    def __init__(self):
        self.body = []
        self.level = 1
        self.create_car()

    def create_car(self):
        """create car and add the car turtle to the fleet of cars"""
        new_car = Car(self.level)
        self.body.append(new_car)

    def refresh(self):
        """at the end of the level clear all the cars in the fleet"""
        for car in self.body:
            car.clear()
            car.reset()
            car.ht()
        self.body = []

class Car(Turtle):
    def __init__(self, level):
        super().__init__()
        self.ht()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.speed("fastest")
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        self.color((r, g, b))
        start_y = randint(LOWER_LIMIT + 50, UPPER_LIMIT - 50)
        self.goto(RIGHT_LIMIT + CAR_LENGTH, start_y)
        self.setheading(180)
        self.move_distance = randint(5 + (2*level), 10 + (2*level))

    def move(self):
        """move car forward"""
        self.forward(self.move_distance)



