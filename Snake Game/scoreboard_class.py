import turtle
from turtle import Turtle, Screen
import time

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.high_score = 0
        self.get_high_score()
        self.refresh()
        self.continue_game = True

    def refresh(self):
        """delete current and high score visuals"""
        self.ht()
        self.penup()
        self.clear()
        self.goto(-50, 200)
        self.write(f"Score: {self.score}", True, align="center", font=("Arial", 12, "normal"))
        self.goto(100, 200)
        self.write(f"High Score: {self.high_score}", True, align="center", font=("Arial", 12, "normal"))

    def get_high_score(self):
        """open 'snake_high_score.txt' in project folder and
            get contents of high score data. The contents of file will be a single integer"""
        try:
            with open("snake_high_score.txt", mode="r") as file:
                contents = file.read()
                self.high_score = int(contents)
        except ValueError:
            with open("snake_high_score.txt", mode="w") as file:
                file.write(str(0))
                self.high_score = 0


    def update_high_score(self):
        """evaluate if end score is greater than high score, if so overwrite
            past high score integer with current high score integer"""
        if self.score > self.high_score:
            self.high_score = self.score
            with open("snake_high_score.txt", mode="w") as file:
                file.write(str(self.high_score))
        self.score = 0


    def game_over(self):
        """sequence for displaying game over text and final score"""
        self.reset()
        self.color("white")
        self.goto(0, 0)
        self.write(f'GAME OVER!\nYour score: {self.score}', True, align="center", font="12")

    def thanks_for_playing(self):
        """sequence for displaying thanks for playing text"""
        self.reset()
        self.color("white")
        self.write(f'Thanks for playing!', True, align="center", font="12")
        time.sleep(5)

    def continue_snake(self):
        """asks the user if they want to continue, changes .continue_game attribute"""
        answers = ['yes', 'no']
        answer = turtle.textinput(prompt='Continue? "yes or no"', title='Game Over').lower()
        if answer not in answers:
            self.continue_snake()
        elif answer == "yes":
            self.continue_game = True
        else:
            self.continue_game = False

    def continue_countdown(self):
        """sequence for displaying a restart countdown"""
        self.reset()
        self.color("white")
        self.write(f'      Game Will Reset in... 3', True, align="center", font="12")
        time.sleep(1)
        self.reset()
        self.color("white")
        self.write(f'      Game Will Reset in... 2', True, align="center", font="12")
        time.sleep(1)
        self.reset()
        self.color("white")
        self.write(f'      Game Will Reset in... 1', True, align="center", font="12")
        time.sleep(1)



