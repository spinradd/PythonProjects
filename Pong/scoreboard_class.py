from turtle import Turtle
import time
from border_class import UPPER_LIMIT, LEFT_LIMIT, RIGHT_LIMIT

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.speed("fastest")
        self.color("white")
        self.ht()
        self.penup()
        self.player_1 = 0
        self.player_2 = 0
        self.refresh()
        self.resume = Turtle(visible=False)
        self.continue_game = True

    def refresh(self):
        """clears scoreboard and rewrites it according to the correct score """
        self.clear()
        self.goto(LEFT_LIMIT, UPPER_LIMIT + 30)
        self.write(f"Player {1}: {self.player_1}", align="left", font=("Arial", 12, "normal"))
        self.goto(LEFT_LIMIT + 100, UPPER_LIMIT + 30)
        self.write(f"w\ns", align="left", font=("Arial", 12, "normal"))
        self.goto(RIGHT_LIMIT, UPPER_LIMIT + 30)
        self.write(f"Player {2}: {self.player_2}", align="right", font=("Arial", 12, "normal"))
        self.goto(RIGHT_LIMIT - 100, UPPER_LIMIT + 30)
        self.write(f"up\ndown", align="right", font=("Arial", 12, "normal"))
        self.goto(0, UPPER_LIMIT + 20)
        self.write("P O N G", align="center", font=("Arial", 30, "normal"))

    def point_scored(self, player):
        """displays text for a point scored"""
        self.resume.ht()
        self.resume.speed("fastest")
        self.resume.penup()
        self.resume.color("white")
        self.resume.goto(0,0)
        self.resume.write(f'Player {player} Scores!!', align="center", font=("Arial", 40, "normal"))
        time.sleep(3)
        self.resume.reset()
        self.resume.ht()

    def resume_game(self):
        """countdown sequence for resuming the game"""
        for n in range(3, 0, -1):
            self.resume.goto(0, 0)
            self.resume.clear()
            self.resume.penup()
            self.resume.color("white")
            self.resume.write(f'Resuming in... {n}', True, align="center", font="12")
            time.sleep(1)
            self.resume.clear()

    def thanks_for_playing(self):
        """a thank you for playing message at the end of the game"""
        thanks = Turtle()
        thanks.speed("fastest")
        thanks.ht()
        thanks.color("white")
        thanks.write(f'Thanks for playing!', True, align="center", font=12)
        time.sleep(5)

    def continue_pong(self):
        """at the end of the game, the funtion displays the final score and gives the players an opportunity
        to close the game"""
        self.clear()
        self.goto(0,15)
        self.write(f"Final Score", True, align="center", font=("Arial", 20, "normal"))
        self.goto(0, -15)
        self.write(f"Player 1: {self.player_1}, Player 2: {self.player_2} ", True, align="center",
                   font=("Arial", 20, "normal"))
        time.sleep(5)
        for n in range(3,0, -1):
            self.goto(0, 10)
            self.clear()
            self.ht()
            self.color("white")
            self.write(f'Press esc to close', True, align="center", font=("Arial", 12, "normal"))
            self.goto(0,-10)
            self.write(f"Game Will Reset in... {n}", True, align="center", font=("Arial", 12, "normal"))
            time.sleep(1)

    def escape(self):
        "sets the continue game attribute of the scoreboard class to False"
        self.continue_game = False