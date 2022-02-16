from question_model import Question
from data import question_data
from quiz_brain import Quiz_Brain
from ui import QuizInterface

# initialize question database
question_bank = []

# questions correct starts at 0
correct_counter = 0

#loop through each question and add question and answer to question bank
for q in question_data:
    question_text = q['question']
    question_answer = q['correct_answer']
    new_q = Question(question_text, question_answer)
    question_bank.append(new_q)

# start quiz with question bank
main_brain = Quiz_Brain(question_bank)

# create gui for quiz
qui_ui = QuizInterface(main_brain)
