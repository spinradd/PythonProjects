import html


class Quiz_Brain:
    # in charge of maintaining list of questions, and checking answers and continuing quiz
    def __init__(self, list_of_questions):
        self.question_number = 0
        self.question_list = list_of_questions

    def still_has_questions(self):
        """check if the numbers of questions answered is less than the total number of questions"""
        if self.question_number < len(self.question_list):
            return True
        else:
            return False

    def next_question(self):
        """loads next question up and displays next question"""
        next_q = self.question_list[self.question_number]
        next_q.text = html.unescape(next_q.text)
        self.question_number += 1
        return f"Q.{self.question_number}: {next_q.text}"

    def check_answer(self, q_answer):
        """check user input T/F versus questions actual answer"""
        if self.question_list[self.question_number -1].answer == q_answer.capitalize():
            return True
        else:
            return False