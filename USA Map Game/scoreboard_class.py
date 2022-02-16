from turtle import RawTurtle
import time
import pandas as pd
from border_class import UPPER_LIMIT, LOWER_LIMIT, LEFT_LIMIT, RIGHT_LIMIT
import tkinter

class Scoreboard(RawTurtle):
    def __init__(self, canv_obj):
        super().__init__(canvas=canv_obj, visible=False)
        self.canvas = canv_obj
        self.ht()
        self.score = 0
        self.min = 0
        self.seconds = 0
        self.timer_label = self.canvas.getcanvas().create_text((LEFT_LIMIT + 150), (-1 * UPPER_LIMIT -39),
                                                            text=f"Time:",
                                                            fill="black", font=("Arial", 12, "normal"))
        self.speed("fastest")
        self.color("white")
        self.pencolor("black")
        self.penup()
        self.refresh()
        self.missing_turt = RawTurtle(canvas=self.canvas, visible=False)
        self.dupli_turt = RawTurtle(canvas=self.canvas, visible=False)
        self.continue_game = True


    def refresh(self):
        """reset scoreboard attributes"""
        self.clear()
        self.goto(LEFT_LIMIT, UPPER_LIMIT + 30)
        self.write(f"Score: {self.score}/50", True, align="left", font=("Arial", 12, "normal"))
        self.goto(LEFT_LIMIT + 100, UPPER_LIMIT + 30)
        self.goto(0, UPPER_LIMIT + 20)
        self.write("U.S.A Test!", True, align="center", font=("Arial", 30, "normal"))

    def not_in_list(self):
        """display not in list message"""
        self.missing_turt.goto(0,0)
        self.missing_turt.ht()
        self.missing_turt.speed("fastest")
        self.missing_turt.penup()
        self.missing_turt.color("black")
        self.missing_turt.write("Sorry, that state doesn't exist!", True, align="center", font=("Arial", 40, "normal"))

    def clear_after_wait(self, turtle_obj):
        """clear board"""
        turtle_obj.clear()
        turtle_obj.ht()

    def already_guessed(self):
        """display already guessed message"""
        self.dupli_turt.goto(0, 0)
        self.dupli_turt.ht()
        self.dupli_turt.speed("fastest")
        self.dupli_turt.penup()
        self.dupli_turt.color("black")
        self.dupli_turt.write("You got that already!", True, align="center", font=("Arial", 40, "normal"))

    def resume_game(self):
        """play resume game message"""
        for n in range(3, 0, -1):
            self.missing_turt.goto(0, 0)
            self.missing_turt.clear()
            self.missing_turt.penup()
            self.missing_turt.color("white")
            self.missing_turt.write(f'Replaying in... {n}', True, align="center", font="12")
            time.sleep(1)
            self.missing_turt.clear()

    def thanks_for_playing(self):
        """display thans for playing message"""
        thanks = RawTurtle(canvas=self.canvas, visible=False)
        thanks.penup()
        thanks.speed("fastest")
        thanks.color("black")
        thanks.write(f'Thanks for playing!', align="center", font=12)
        time.sleep(5)

    def display_score(self):
        """display scorecard on top of the screen"""
        self.clear()
        self.goto(0, 15)
        score_in_string = time.strftime("%M:%S", time.gmtime(self.timed_val))
        self.write(f"Final Score:", True, align="center", font=("Arial", 20, "normal"))
        self.goto(0, -15)
        self.write(f"{self.score}/50 ", True, align="center", font=("Arial", 20, "normal"))
        self.goto(0, -45)
        self.write(f"{score_in_string} ", True, align="center", font=("Arial", 20, "normal"))
        time.sleep(5)

    def continue_quiz(self, screen_obj):
        """ask user if they want to continue the quiz or quit"""
        valid_responses = ["yes", "no"]
        while self.continue_game not in valid_responses:
            try:
                self.continue_game = screen_obj.textinput(title="Continue?", prompt="Play again? yes or no").lower()
            except AttributeError:
                return False
        if self.continue_game == "yes":
            return True
        else:
            return False

    def read_high_score(self):
        """get high score data from text file"""
        self.high_score_data = pd.read_csv("high_score.csv")

    def display_high_scores(self):
        """display list of high scores from text file"""
        high_scores = ""
        for index, row in self.high_score_data.iterrows():
            high_scores = high_scores + (f"{row['name']} {time.strftime('%M:%S', time.gmtime(row['time in seconds']))}\n")
        new_high = RawTurtle(canvas=self.canvas, visible=False)
        new_high.ht()
        new_high.speed("fastest")
        new_high.penup()
        new_high.goto(0, 100)
        new_high.write("High Scores", align="center", font=("Arial", 20, "normal"))
        new_high.goto(0, 0)
        new_high.write(f"{high_scores}", align="center", font=("Arial", 12, "normal"))
        time.sleep(5)
        new_high.clear()

    def is_new_high_score(self):
        """evaluate if new score is the new high score"""
        highest_score_row = self.high_score_data[self.high_score_data["time in seconds"] == self.high_score_data["time in seconds"].min()]
        highest_score_val = float(highest_score_row["time in seconds"])
        if self.timed_val < highest_score_val and self.score == 1:
            return True

    def write_high_score(self):
        """write new high score to text file"""
        new_high_score = RawTurtle(canvas=self.canvas, visible=False)
        new_high_score.ht()
        new_high_score.speed("fastest")
        new_high_score.penup()
        new_high_score.write(f"NEW HIGH SCORE", align="center", font=("Arial", 40, "normal"))
        time.sleep(3)
        new_high_score.clear()
        name = self.screen.textinput(title="Nice!", prompt="What is your name?").capitalize()
        self.high_score_data = self.high_score_data.append({"name": name, "time in seconds": self.timed_val}, ignore_index=True)
        self.high_score_data = self.high_score_data.sort_values("time in seconds", ascending=True)
        self.high_score_data.to_csv("high_score.csv", index=False)

