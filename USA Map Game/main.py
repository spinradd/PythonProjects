from screen_class import Window
import math
import tkinter as tk
import pandas as pd
from scoreboard_class import Scoreboard
from border_class import Border
from label_class import Labels

# initialize root and other classes
root = tk.Tk()
window = Window(root)
border = Border(window.screen)
scoreboard = Scoreboard(window.screen)
game_timer = None
num_states = 50


def update_timer():
    """add one second to the timer count, convert to mm:ss format, update timer"""
    global num_states
    scoreboard.seconds += 1
    scoreboard.min = math.floor(scoreboard.seconds / 60)
    seconds = scoreboard.seconds
    if scoreboard.seconds < 10:
        seconds = f"0{scoreboard.seconds}"
    window.canvas.itemconfig(scoreboard.timer_label, text=f"Time: {scoreboard.min}:{seconds}")
    if scoreboard.score < num_states:
        root.after(1000, update_timer)


# initialize timer
update_timer()

# initialize other game attributes, get state data fro file
labels = Labels(window.screen)
state_data = pd.read_csv("50_states.csv")
window.screen.listen()
window.screen.onkey(root.destroy, "Escape")
labels.body = []
scoreboard.score = 0


def play_game():
    answer_state = None
    if scoreboard.continue_game:

        # if states guessed < 50, continue
        if scoreboard.score < num_states:

            # try to get user input, if blank assume no state
            try:
                answer_state = window.screen.textinput(title="Guess a state",
                                                       prompt='Whats another state name? (or "quit")').title()
            except AttributeError:
                answer_state == None

            # if user input is quit or none, destroy canvas
            if answer_state == "Quit" or answer_state == None:
                root.destroy()

            # if user input exists within states database
            if answer_state in state_data.state.values:

                # if input wasn't already guessed, add to guessed list, increase scoreboard, reset canvas
                if answer_state not in labels.guessed_list:
                    labels.guessed_list.append(answer_state)
                    scoreboard.score += 1
                    scoreboard.refresh()

                    # find row of state guessed, extract x and y coordinates
                    row = state_data[state_data.state == answer_state]
                    x = int(row.x)
                    y = int(row.y)

                    # create state label, continue game
                    labels.create_label(answer_state, x, y)
                    play_game()

                # if input was already guessed, display 'already guessed' message, clear screen and reset
                else:
                    for turtles in labels.body:
                        try:
                            if turtles.state_name != answer_state:
                                turtles.clear()
                        except AttributeError:
                            None
                    scoreboard.already_guessed()
                    root.after(3000, scoreboard.clear_after_wait, scoreboard.dupli_turt)
                    root.after(3000, play_game)

            # if answer is not in database display 'not valid' message
            else:
                for turtles in labels.body:
                    turtles.clear()
                scoreboard.not_in_list()
                root.after(3000, scoreboard.clear_after_wait, scoreboard.missing_turt)
                root.after(3000, play_game)

        # if num of states guessed is 50, end game
        else:

            # clear all turtles
            for turtles in labels.body:
                turtles.clear()
            # calculated final time in seconds
            scoreboard.timed_val = scoreboard.min * 60 + scoreboard.seconds
            # read high score
            scoreboard.read_high_score()

            # if new score is greater than high score, write new score
            if scoreboard.is_new_high_score():
                scoreboard.write_high_score()

            # display all high scores
            scoreboard.display_high_scores()

            # prompt user for replay, if yes reset window
            if scoreboard.continue_quiz(window.screen):
                scoreboard.continue_game = True
                for turtles in labels.body:
                    turtles.clear()
                labels.body = []
                scoreboard.seconds = 0
                scoreboard.score = 0
                scoreboard.refresh()
                border.create_border()
                update_timer()
                play_game()

            # if user wants to end the game, delete everything, restarts
            else:
                scoreboard.continue_game = False
                for turtles in window.screen.turtles():
                    turtles.clear()
            play_game()
    else:
        root.destroy()


play_game()

window.screen.mainloop()