from tkinter import *
from quiz_brain import Quiz_Brain
import time

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: Quiz_Brain):
        self.quiz = quiz_brain
        WINDOW_W = 300
        WINDOW_H = 400
        CANVAS_H = 250
        CANVAS_W = 300

        self.window = Tk()
        self.window.title("Quizlet")
        self.window.config(bg=THEME_COLOR,
                           height=WINDOW_H, width=WINDOW_W,
                           pady=20)
        self.window.lift()
        self.canv = Canvas(height=CANVAS_H, width=CANVAS_W)
        self.canv.config(bg="white", highlightthickness=0,)
        self.canv.grid(column=0, row=1, columnspan=2, padx=20, pady=20)
        self.score_count = 0
        self.score_label = Label(text=f"Score: {self.score_count}", fg="white", bg=THEME_COLOR, font=("Arial", 12, "normal"))
        self.score_label.grid(column=1, row=0, pady=20)
        wrong_img = PhotoImage(file="images/false.png")
        self.false_button = Button(image=wrong_img, highlightthickness=0, bg=THEME_COLOR, pady=20,
                                   command=self.false_pressed)
        self.false_button.grid(column=1, row=2)
        right_img = PhotoImage(file="images/true.png")
        self.true_button = Button(image=right_img, highlightthickness=0, bg=THEME_COLOR, pady=20,
                                  command=self.true_pressed)
        self.true_button.grid(column=0, row=2)
        self.question_text = self.canv.create_text(round(CANVAS_W/2), round(CANVAS_H/2),
                                                   text="No Questions Primed",
                                                   font=("Arial", 20, "italic"),
                                                   tags="word",
                                                   width=(CANVAS_W-10))
        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        """load next questions onto user interface"""
        self.canv.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canv.itemconfig(self.question_text, text=q_text)
        else:
            self.canv.itemconfig(self.question_text, text="You've reached the end of the quiz!")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_pressed(self):
        """if True button is pressed send true value to check answer function"""
        is_correct = self.quiz.check_answer("true")
        self.give_feedback(is_correct)

    def false_pressed(self):
        """if False button is pressed send false value to check answer function"""
        is_correct = self.quiz.check_answer("false")
        self.give_feedback(is_correct)

    def give_feedback(self, bool):
        """takes in user input and evaluates answer. If correct flash green, else red"""
        if bool:
            self.canv.config(bg="green")
            self.score_count += 1
            self.score_label.config(text=f"Score: {self.score_count}")
        else:
            self.canv.config(bg="red")
        self.window.after(1000, self.get_next_question)