from turtle import Turtle

MOVING_VALUE = 20
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]

class Snake(Turtle):
    def __init__(self):
        super().__init__()
        self.body = []
        self.create_snake()
        self.snake_head = self.body[0]

    def create_snake(self):
        """create body of snake"""
        for pos in STARTING_POSITIONS:
            self.add_segment(pos)

    def add_segment(self, position):
        """adds extra square or body piece to main snake list"""
        segment = Turtle(shape="square", visible=True)
        segment.color("white")
        segment.penup()
        segment.goto(position)
        self.body.append(segment)


    def extend(self):
        """extra function to add segment of snake after food is eaten -
        piece is added at the end of the body"""
        self.add_segment(self.body[-1].position())


    def move(self):
        """For each piece in the snake body, move the piece to the location of the one before it (starting from
        the end of the body), then set the piece's heading to match the one before it as well"""
        for segment in self.body[:0:-1]:
            segment.setx(self.body[(self.body.index(segment) - 1)].xcor())
            segment.sety(self.body[(self.body.index(segment) - 1)].ycor())
            segment.setheading(self.body[(self.body.index(segment) - 1)].heading())
        self.body[0].forward(MOVING_VALUE)

    def up(self):
        """rotate the snake head to face up"""
        if self.snake_head.heading() != 270 and self.body[1].heading() != 270:
            self.snake_head.setheading(90)

    def left(self):
        """rotate the snake head to face left"""
        if self.snake_head.heading() != 0 and self.body[1].heading() != 0:
            self.snake_head.setheading(180)

    def down(self):
        """rotate the snake head to face down"""
        if self.snake_head.heading() != 90 and self.body[1].heading() != 90:
            self.snake_head.setheading(270)

    def right(self):
        """rotate the snake head to face right"""
        if self.snake_head.heading() != 180 and self.body[1].heading() != 180:
            self.snake_head.setheading(0)

    def delete_snake(self):
        """delete snack if player loses"""
        for segment in self.body:
            segment.reset()

    def snake_collision(self):
        """detect when snake collides ith itself"""
        for segments in self.body[1:]:
            if self.snake_head.distance(segments) <= 10:
                return True
        return False

    def refresh(self):
        """resets snake body at beginning of new game"""
        self.body = []
        self.create_snake()
        self.snake_head = self.body[0]




