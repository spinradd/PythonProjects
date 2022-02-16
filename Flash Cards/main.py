import tkinter.messagebox
from tkinter import *
from PIL import Image, ImageTk
import pandas
import random
import csv

BACKGROUND_COLOR = "#B1DDC6"
language_word = None
english_word = None
german_word = None
to_learn_dataframe = pandas.DataFrame()

# ------------------------- Read DataFiles, create mastered dictionary --------------------------


def read_frequency_dict():
    """read words from frequency dictionary"""
    try:
        with open("data/learn_german.csv", "w+") as to_learn_file:
            None
        df = pandas.read_csv("data/german_words.csv")
        return df
    except FileNotFoundError:
        raise Exception('No data or file found in "data/german_words.csv" filepath')

# ------------------------- Evaluate if language text files exist, ask user if they want to reset their "mastered" list --------------------------


# try to read file of language words
# if file doesn't exist, ask user to create a file
# finally, ask user if they want to reset their "mastered" words list
try:
    to_learn_dataframe = pandas.read_csv("data/learn_german.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError) as e:
    create = tkinter.messagebox.askyesno(title="Create to continue?", message=('There is currently no dictionary to populate flash cards. Should we create it?'))
    if not create:
        exit()
    elif create:
        to_learn_dataframe = read_frequency_dict()
finally:
    reset_dictionary = tkinter.messagebox.askyesno(title="Reset?", message=('Would you like to reset your mastered word list to 0?'))
    if reset_dictionary:
        to_learn_dataframe = read_frequency_dict()
    to_learn_dict = {row.German: row.English for (key, row) in to_learn_dataframe.iterrows()}

# read from mastered list, if file not found, create one

try:
    mastered_dataframe = pandas.read_csv("data/mastered_german_words.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError) as e:
    with open("data/mastered_german_words.csv", "w+") as mastered_file:
        mastered_dict = {"Deutsch": "German"}
else:
    mastered_dict = {row.German: row.English for (key, row) in mastered_dataframe.iterrows()}

# ------------------------- Pull Up New Card --------------------------#


def generate_new_words():
    """pulls a german word and its english translation, and removes it from
       the dictionary to avoid a potential repeat"""
    global language_word
    global german_word
    global english_word
    language_word = "German"
    german_word = random.choice(list(to_learn_dict))
    english_word = to_learn_dict[german_word]


def update_card():
    """takes current language, german word, and english word and displays appropriate card"""
    if language_word == "German":
        canv.itemconfig(side, image=front_photo)
        word = german_word
    else:
        canv.itemconfig(side, image=back_photo)
        word = english_word
    try:
        canv.delete("language")
        canv.delete("word")
    finally:
        canv.create_text(round(WINDOW_W / 2), 75, text=language_word, font=("Arial", 15, "normal"), tags="language")
        canv.create_text(round(WINDOW_W / 2), round(WINDOW_H / 2), text=word, font=("Arial", 20, "bold"), tags="word")

def flip_card():
    global language_word
    """if card is currently german, change background and display english, and vice versa"""
    if canv.itemcget("language", "text") == "German":
        canv.itemconfig(side, image=back_photo)
        language_word = "English"
    else:
        canv.itemconfig(side, image=front_photo)
        language_word = "German"

    update_card()
# ------------------------- got card correct --------------------------


def add_to_mastered_delete_from_learning():
    """fun will add correctly known word to mastered_dict, will erase pair from still
        learning dict"""
    mastered_dict[german_word] = english_word
    del to_learn_dict[german_word]
# ------------------------- when program closes, update CSV --------------------------


def on_close():
    """Update mastered cvs and to learn csv"""
    mastered_data = {"German": mastered_dict.keys(), "English": mastered_dict.values()}
    to_learn_data = {"German": to_learn_dict.keys(), "English": to_learn_dict.values()}
    mastered_dataframe_final = pandas.DataFrame.from_dict(mastered_data)
    to_learn_dataframe_final = pandas.DataFrame.from_dict(to_learn_data)
    filepath_mastered = "data/mastered_german_words.csv"
    filepath_to_learn = "data/learn_german.csv"
    with open(filepath_mastered, "w", encoding="UTF-8") as m_file:
        mastered_dataframe_final.to_csv(m_file, line_terminator='\n', index=False)
    with open(filepath_to_learn, "w", encoding="UTF-8") as tl_file:
        to_learn_dataframe_final.to_csv(tl_file, line_terminator='\n', index=False)
    window.destroy()
# ------------------------- UI interface --------------------------

WINDOW_W = 600
WINDOW_H = 326

# create window
window = Tk()
window.title("German Flash Cards")
window.config(bg =BACKGROUND_COLOR, padx=20, pady=20)
window.lift()

# canvas
canv = Canvas(height=WINDOW_H, width=WINDOW_W)
canv.config(bg=BACKGROUND_COLOR, highlightthickness=0)
# resize images
front_side = Image.open("images/card_front.png")
resized_front = front_side.resize((WINDOW_W, WINDOW_H), Image.ANTIALIAS)
front_photo = ImageTk.PhotoImage(resized_front)

back_side = Image.open("images/card_back.png")
resized_back = back_side.resize((WINDOW_W, WINDOW_H), Image.ANTIALIAS)
back_photo = ImageTk.PhotoImage(resized_back)

side = canv.create_image(0, 0, anchor=NW,  image=front_photo, tags="card_side")
canv.grid(column=0, row=0, columnspan=3)

# create first card
generate_new_words()
update_card()

# wrong button
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR,
                      command= lambda: (generate_new_words(), update_card()))
wrong_button.grid(column=0, row=2)

# right button
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR,
                      command= lambda: (add_to_mastered_delete_from_learning(), generate_new_words(), update_card()))
right_button.grid(column=2, row=2)

# flip button
flip_button = Button(window, text="Flip!", highlightthickness=10, bg="white", command=flip_card)
flip_button.config(width=2, height=1)
flip_button.grid(column=1, row=1)

window.protocol("WM_DELETE_WINDOW", lambda: on_close())
window.mainloop()