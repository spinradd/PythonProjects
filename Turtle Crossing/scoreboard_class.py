from turtle import Turtle
import time
from border_class import UPPER_LIMIT, LEFT_LIMIT, PIXEL_WIDTH

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.ht()
        self.level = 1
        self.speed("fastest")
        self.color("black")
        self.penup()
        self.refresh()
        self.level_up = Turtle(visible=False)
        self.continue_game = True

    def refresh(self):
        """reset canvas as the start of a new level or new game"""
        self.clear()
        self.penup()
        self.ht()
        self.goto(LEFT_LIMIT+10+PIXEL_WIDTH, UPPER_LIMIT+10+PIXEL_WIDTH)
        self.write(f"Level - {self.level}", True, align="center", font=("Arial", 12, "normal"))
        self.color("green")
        self.goto(-85, UPPER_LIMIT + 15)
        self.write(f"Turtle", True, align="center", font=("Arial", 35, "normal"))
        self.goto(85, UPPER_LIMIT + 15)
        self.write(f"Crossing", True, align="center", font=("Arial", 35, "italic"))
        self.color("black")

    def next_level(self):
        """when the level is beaten, write "Success" """
        self.level_up.ht()
        self.level_up.speed("fastest")
        self.level_up.penup()
        self.level_up.color("black")
        self.level_up.write("Success!", True, align="center", font=("Arial", 35, "normal"))
        time.sleep(3)
        self.level_up.reset()
        self.level_up.clear()
        self.level_up.ht()

    def resume_game(self):
        """countdown for the beginning of a new level"""
        for n in range(3, 0, -1):
            self.level_up.goto(0, 0)
            self.level_up.clear()
            self.level_up.penup()
            self.level_up.color("white")
            self.level_up.write(f'Resuming in... {n}', True, align="center", font="12")
            time.sleep(1)
            self.level_up.clear()

    def thanks_for_playing(self):
        """a thank you for playing sign"""
        thanks = Turtle()
        thanks.speed("fastest")
        thanks.ht()
        thanks.color("white")
        thanks.write(f'Thanks for playing!', True, align="center", font=12)
        time.sleep(5)

    def continue_crossing(self):
        """lets the user know they can continue playing or press escape to end"""
        self.clear()
        self.ht()
        self.goto(0,0)
        self.write(f"You got to level {self.level}", True, align="center", font=("Arial", 20, "normal"))
        time.sleep(3)
        for n in range(3,0, -1):
            self.goto(0, 10)
            self.clear()
            self.ht()
            self.color("black")
            self.write(f'Press esc to close', True, align="center", font=("Arial", 12, "normal"))
            self.goto(0,-10)
            self.write(f"Game Will Reset in... {n}", True, align="center", font=("Arial", 12, "normal"))
            time.sleep(1)


    def escape(self):
        """sets continue game to False"""
        self.continue_game = False