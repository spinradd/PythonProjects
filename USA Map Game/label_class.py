from turtle import RawTurtle
import math

class Labels(RawTurtle):
    def __init__(self, canv_obj):
        super().__init__(canvas=canv_obj, visible=False)
        self.canvas = canv_obj
        self.body = []
        self.guessed_list = []

    def create_label(self, state, x_cor, y_cor):
        """create a sate label move turtle label to state position"""
        label = RawTurtle(canvas=self.canvas, visible=True)
        label.penup()
        label.speed(1)
        label.color("black")
        label.state_name = state
        label.x = int(x_cor)
        label.y = int(y_cor)
        heading = math.degrees(math.atan(label.y / label.x))

        # fix turtle pointer heading depending on where the state label is located
        if label.x < 0 and label.y < 0:
            heading = heading + 180
        elif label.x < 0:
            heading *= -1
            heading += 90
        elif label.y < 0:
            heading *= -1
            heading = 360 - heading

        # set calculated heading
        label.setheading(heading)
        label.goto(label.x, label.y)
        label.write(label.state_name, align="center", font=("Arial", 12, "normal"))
        self.body.append(label)
        label.ht()

    def place_label(self, label_obj):
        """if map is cleared, replace labels where they are"""
        label_obj.ht()
        label_obj.speed("fastest")
        label_obj.goto(label_obj.x, label_obj.y)
        label_obj.write(label_obj.state_name, align="center", font=("Arial", 12, "normal"))

    def repopulate_map(self):
        """method for replacing all the labels"""
        for label in self.body:
            self.place_label(label)