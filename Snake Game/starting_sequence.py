from turtle import Turtle
import time

UP = "w"
DOWN = "s"
LEFT = "a"
RIGHT = "d"

class Start_Class(Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.color("white")
        self.speed("fastest")
        self.up = UP
        self.down = DOWN
        self.left = LEFT
        self.right = RIGHT

    def create_keyboard(self):
        """create 'w, a, s, d' text in top right corner of the screen"""
        self.ht()
        self.penup()
        self.clear()
        self.goto(-240, 200)
        self.write(f"    {self.up}\n{self.left}, {self.down}, {self.right}", True, align="center", font="6")

    def display_sequence(self):
        """sequence to display starting countdown text"""
        self.penup()
        self.clear()
        self.ht()
        self.goto(0,0)
        for n in range(3,0,-1):
            self.write(f"{n}", True, align="center", font="12")
            self.goto(0, 0)
            time.sleep(1)
            self.clear()


