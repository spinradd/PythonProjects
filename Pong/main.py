from turtle import Screen
import ball_class
from paddles import Paddle, PADDLE_WIDTH, PADDLE_HEIGHT
from border_class import Border, WINDOW_HEIGHT, WINDOW_WIDTH, PIXEL_WIDTH, LEFT_LIMIT, RIGHT_LIMIT
from scoreboard_class import Scoreboard
from ball_class import Ball


TOP_SCORE = 3

# initialize screen
window = Screen()
window.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
window.colormode(255)
window.title("PONG !")
window.bgcolor("black")
window.tracer(False)
window.listen()

# create turtle classes
board = Scoreboard()
border = Border()
left_paddle = Paddle()
left_paddle.create_left()
right_paddle = Paddle()
right_paddle.create_right()
ball = Ball()
ball.ht()

# initialize key machine for two player function
keys_machine = {}


def key_pressed(event):
    """return true when button pressed"""
    keys_machine[event.keysym] = True


def key_released(event):
    """return false when button not pressed"""
    keys_machine[event.keysym] = False


def set_keys():
    """for each key, pair press and release of key with true and false.
     set each key to false (released)"""
    for key in ["Up", "Down", "w", "s"]:
        window.getcanvas().bind(f"<KeyPress-{key}>", key_pressed)
        window.getcanvas().bind(f"<KeyRelease-{key}>", key_released)
        keys_machine[key] = False

# pair keys
set_keys()

window.onkey(window.bye, "Escape")
window.tracer(True)

#while playing the game
keep_playing = True

while keep_playing:

    # reset ball and paddles to starting position
    board.resume_game()

    #while there is no winner
    while board.player_1 < TOP_SCORE and board.player_2 < TOP_SCORE:

        # pair keys to movements
        if keys_machine["Up"]: right_paddle.move_up()
        if keys_machine["Down"]: right_paddle.move_down()
        if keys_machine["w"]: left_paddle.move_up()
        if keys_machine["s"]: left_paddle.move_down()

        # show paddles and ball
        left_paddle.st()
        right_paddle.st()
        ball.st()

        # begin ball movement
        ball.move()

        # evaluate if ball has hit paddle, border, or been scored with
        if ball.distance(right_paddle) < (PADDLE_HEIGHT/2) + PIXEL_WIDTH and ball.xcor() > RIGHT_LIMIT - (2 * PADDLE_WIDTH): #paddle hit
            ball.paddle_bounce(right_paddle)
        elif ball.distance(left_paddle) < (PADDLE_HEIGHT/2) + PIXEL_WIDTH and ball.xcor() < LEFT_LIMIT + (2 * PADDLE_WIDTH):
            ball.paddle_bounce(left_paddle)

        # if ball has been scored on the right paddle, stop play, show score, reset game
        elif ball.distance(right_paddle) > (PADDLE_HEIGHT/2) + PIXEL_WIDTH  and ball.xcor() > RIGHT_LIMIT - (2 * PADDLE_WIDTH): #paddle missed point scored
            board.player_1 += 1
            left_paddle.ht()
            right_paddle.ht()
            left_paddle.goto(LEFT_LIMIT, 0)
            right_paddle.goto(RIGHT_LIMIT, 0)
            ball.ht()
            ball.goto(0, 0)
            board.refresh()
            board.point_scored(1)
            ball.x_movement = ball_class.BALL_PPF
            ball.y_movement = ball_class.BALL_PPF

            # if score does not breach limit, return components to starting position, continue
            if board.player_1 < TOP_SCORE and board.player_2 < TOP_SCORE:
                board.resume_game()
            continue
        # if ball has been scored on the left paddle, stop play, show score, reset game
        elif ball.distance(left_paddle) > (PADDLE_HEIGHT/2) + PIXEL_WIDTH and ball.xcor() < LEFT_LIMIT + (2 * PADDLE_WIDTH):
            board.player_2 += 1
            left_paddle.ht()
            right_paddle.ht()
            left_paddle.goto(LEFT_LIMIT, 0)
            right_paddle.goto(RIGHT_LIMIT, 0)
            ball.ht()
            ball.goto(0, 0)
            board.refresh()
            board.point_scored(2)
            ball.x_movement = ball_class.BALL_PPF
            ball.y_movement = ball_class.BALL_PPF
            if board.player_1 < TOP_SCORE and board.player_2 < TOP_SCORE:
                board.resume_game()
            continue

    # hide paddle and ball if game is over
    left_paddle.ht()
    right_paddle.ht()
    ball.ht()

    # prompt for replay
    board.continue_pong()

    # if end game, end game
    if not board.continue_game:
        keep_playing = False
    # if keep playing, reset game
    else:
        board.player_1 = 0
        board.player_2 = 0
        board.refresh()


#end sequences
board.thanks_for_playing()
board.bye()

window.exitonclick()