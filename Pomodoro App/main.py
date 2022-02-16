from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
loop = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 

def click_reset():
    """click reset to reset pomodoro progress"""
    global loop
    window.after_cancel(timer)
    loop = 0
    checkbox.config(text="")
    timer_label.config(text="Timer", fg="black")
    canvas.itemconfig(timer_text, text=f"00:00")

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def click_start():
    """click start to start the timer and the pomodoro process 25/5 intervals"""
    global loop
    loop += 1
    if loop % 8 == 0:
        start = LONG_BREAK_MIN * 60
        timer_label.config(fg=GREEN, text="Break")
    elif loop % 2 == 0:
        start = SHORT_BREAK_MIN * 60
        timer_label.config(fg=GREEN, text="Break")
    else:
        start = WORK_MIN * 60
        timer_label.config(fg=RED, text="Work")
    countdown(start)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def countdown(count):
    """timer counts down one second"""
    global timer
    min = math.floor(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    canvas.itemconfig(timer_text, text=f"{min}:{seconds}")
    if count >= 0:
        timer = window.after(1000, countdown, count -1)
    else:
        checkbox_string = "✓"
        checkbox_display = ""
        for n in range(0, loop % 2):
            checkbox_display = checkbox_display + checkbox_string
        checkbox.config(text=checkbox_display)
        click_start()


# ---------------------------- UI SETUP ------------------------------- #

# initialize pomodoro window
window_width = 200
window_height = 224
window = Tk()
window.minsize(width=window_width, height=window_height)
window.config(padx=100, pady=50, bg=YELLOW)

# create canvas
canvas = Canvas(width=window_width, height=window_height, bg=YELLOW, highlightthickness=0)
photo = PhotoImage(file="tomato.png")
canvas.create_image((window_width/2), (window_height/2), image=photo)
timer_text = canvas.create_text((window_width/2), (window_height/2)+20, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# create label
timer_label = Label(text="Timer", font=(FONT_NAME, 30, "normal"), fg="black", bg=YELLOW)
timer_label.grid(column=1, row=0)

# start_button
start_button = Button(text="Start", command=click_start)
start_button.config(width=10, height=1)
start_button.grid(column=0, row=2)

# reset button
reset_button = Button(text="Reset", command=click_reset)
reset_button.config(width=10, height=1)
reset_button.grid(column=2, row=2)

# checkboxes
checkbox = Label(bg=YELLOW)
checkbox.config(padx=5, pady=10)
checkbox.grid(column=1, row=2)

window.mainloop()


