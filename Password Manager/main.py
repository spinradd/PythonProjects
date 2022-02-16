from tkinter import *
import random
from tkinter import messagebox
import pyperclip
import json

YOUR_EMAIL = "EXAMPLE_EMAIL@FAKE.COM"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """randomizes characters for password, returns final password as string"""
    special_char = "!@#$%^&*()_-+={}[]\<>?/"
    letters = "abcdefghijklmnopqrstuvwxyz"
    numbers= "0123456789"
    char_types = ["special_char", "letters", "numbers"]
    password = ""

    #create password with 10 characters in length
    for n in range(0,10):
        char_type = random.choice(char_types)
        if char_type == "letters":
            capital_letter = random.choice(["titlecase", "lowercase"])
            if capital_letter == "lowercase":
                char = random.choice(list(letters)).lower()
            else:
                char = random.choice(list(letters)).upper()
        elif char_type == "special_char":
            char = random.choice(list(special_char))
        elif char_type == "numbers":
            char = random.choice(list(numbers))
        password = password + char
    pass_entry.delete(0, END)
    pass_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_password(website, email, password):
    """if website, email, or password is blank, show error and exit function -
    if info is present, add info to the JSON file"""
    if len(website) == 0:
        messagebox.showerror(title="Error", message="Empty website")
        return 0
    elif len(email) == 0:
        messagebox.showerror(title="Error", message="Empty email")
        return 0
    elif len(password) == 0:
        messagebox.showerror(title="Error", message="Empty password")
        return 0

    pop_up = messagebox.askokcancel(title=website, message=(f"These are the details entered:\n"
                                                  f"Email: {email}\n"))

    # if verification pop up yields false (cancel), exit fun
    if not pop_up:
        return 0

    # format new data into JSON
    new_data = {
        website.upper(): {
        "email": email,
        "password": password}
    }

    # check if file exists, if not create
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            data.update(new_data)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open("data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
    else:
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
    finally:
        pass_entry.delete(0, END)
        web_entry.delete(0, END)

# ---------------------------- Search --------------------------------- #


def search(website):
    """pull up JSON data, if not found display error, if found populate requested email/password"""
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showerror(title="Error", message="No passwords to search, need to initialize file (add passwords).")

    else:
        try:
            password = data[website]["password"]
            email = data[website]["email"]
        except KeyError:
            messagebox.showerror(title="Error", message="Website not found.")
            pass_entry.delete(0, END)
        else:
            pass_entry.delete(0, END)
            email_entry.delete(0, END)
            pass_entry.insert(END, password)
            email_entry.insert(END, email)


# ---------------------------- UI SETUP ------------------------------- #


WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
PAD_BETWEEN_ROWS = 5
ENTRY_WIDTH = 35

# window
window = Tk()
window.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
window.config(padx=50, pady=50, bg="white")
window.title("Password Manager")

# canvas
canv = Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white", highlightbackground="black", highlightthickness=2)
photo = PhotoImage(file="logo.png")
canv.create_image((WINDOW_WIDTH/2), (WINDOW_HEIGHT/2), image=photo)
canv.grid(column=1, row=0)

# web label and entry
web_label = Label(text="Website:", bg="white")
web_label.grid(column=0, row=1, pady=PAD_BETWEEN_ROWS)

web_entry = Entry(width=ENTRY_WIDTH)
web_entry.focus()
web_entry.grid(column=1, row=1, columnspan=1, pady=PAD_BETWEEN_ROWS, sticky="we")

# web button, present in frame
web_frame = Frame(window, width=100, height=25, highlightcolor="black")
web_frame.grid_propagate(False)
web_frame.columnconfigure(0, weight=1)
web_frame.rowconfigure(0, weight=1)
web_frame.grid(column=2, row=1)

web_button = Button(web_frame, text="Search", command= lambda: search(web_entry.get().upper()))
web_button.config(width=14, pady=PAD_BETWEEN_ROWS, highlightthickness=0)
web_button.grid(column=0, row=0, sticky="wens")


# email label and entry
email_label = Label(text="Email/Username:", bg="white")
email_label.grid(column=0, row=2, pady=PAD_BETWEEN_ROWS)

email_entry = Entry(width=ENTRY_WIDTH)
email_entry.insert(END, string=YOUR_EMAIL)
email_entry.grid(column=1, row=2, columnspan=2, pady=PAD_BETWEEN_ROWS, sticky="we")

# password label and entry
pass_label = Label(text="Password:", bg="white")
pass_label.grid(column=0, row=3, pady=PAD_BETWEEN_ROWS, sticky="we")

pass_entry = Entry(width=21)
pass_entry.grid(column=1, row=3, pady=PAD_BETWEEN_ROWS, sticky="we")

# password_button, present in frame
pass_frame = Frame(window, width=100, height=25, highlightcolor="black")
pass_frame.grid_propagate(False)
pass_frame.columnconfigure(0, weight=1)
pass_frame.rowconfigure(0, weight=1)
pass_frame.grid(column=2, row=3)

pass_button = Button(pass_frame, font =("Arial", 8, "normal"), text="Generate Password", command=generate_password)
pass_button.config(width=14, pady=PAD_BETWEEN_ROWS, highlightthickness=0)
pass_button.grid(column=0, row=0, sticky="nsew")

# add_button
add_frame = Frame(window, width=100, height=25, highlightcolor="black")
add_frame.grid_propagate(False)
add_frame.columnconfigure(0, weight=1)
add_frame.rowconfigure(0, weight=1)
add_frame.grid(column=1, row=4, columnspan=2, sticky="ew")
add_button = Button(add_frame, text="Add", command= lambda: add_password(web_entry.get(), email_entry.get(), pass_entry.get()))
add_button.config(width=36, pady=PAD_BETWEEN_ROWS, highlightthickness=0)
add_button.grid(column=0, row=0, sticky="nsew")


window.mainloop()