from turtle import Turtle, Screen
from border_class import Border, WINDOW_WIDTH, WINDOW_HEIGHT, UPPER_LIMIT
from character import Player, PLAYER_HEIGHT
from car_class import Fleet, CAR_LENGTH, CAR_HEIGHT
from scoreboard_class import Scoreboard
import time

#initialize screen
window = Screen()
window.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
window.colormode(255)
window.title("Turtle Crossing!")
window.listen()

#initialize class objects
border = Border()
player = Player()
scoreboard = Scoreboard()
fleet = Fleet()

#initialize keys machine
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
    for key in ["a", "s", "d", "w"]:
        window.getcanvas().bind(f"<KeyPress-{key}>", key_pressed)
        window.getcanvas().bind(f"<KeyRelease-{key}>", key_released)
        keys_machine[key] = False


# pair keys
set_keys()
window.onkey(window.bye, "Escape")

window.tracer(False)

# start at level 0
loop = 0
while scoreboard.continue_game:

    # assume game over is false
    game_over = False

    # while game is being played, spawn and move cars
    while not game_over:
        time.sleep(.01)

        # pair key functions to turtle movements
        if keys_machine["w"]: player.move_up()
        if keys_machine["s"]: player.move_down()
        if keys_machine["a"]: player.move_left()
        if keys_machine["d"]: player.move_right()

        # after movement update screen
        window.update()

        # increase loop, sleep, and update
        loop += 1
        time.sleep(.05)
        window.update()

        # when loop is divisible by 5, create car
        if loop % 5 == 0:
            fleet.create_car()

        # for every car that exists, move the car
        for car in fleet.body:
            car.st()
            car.move()

            #if player is hit by car, game over
            if player.distance(car) < ((CAR_LENGTH / 2)) and \
                (car.ycor() - (CAR_HEIGHT / 2) < player.ycor() + (PLAYER_HEIGHT / 2) < car.ycor() + (CAR_HEIGHT / 2) \
                or car.ycor() - (CAR_HEIGHT / 2) < player.ycor() - (PLAYER_HEIGHT / 2) < car.ycor() + (CAR_HEIGHT / 2)):
                game_over = True
                break

        # if the game is over, continue
        if game_over:
            continue

        #if player reaches end of the road, reset canvas, increase difficulty and restart
        if player.ycor() > UPPER_LIMIT:
            scoreboard.refresh()
            fleet.refresh()
            player.refresh()
            scoreboard.next_level()
            next_level = True
            fleet.level += 1
            scoreboard.level += 1
            continue

    # when game is over, prompt for a restart or to end the game
    scoreboard.continue_crossing()

    # if game over, continue, exit loop
    if not scoreboard.continue_game:
        continue

    # if not game over, reset level and reset canvas
    else:
        scoreboard.level = 0
        scoreboard.refresh()
        fleet.refresh()
        player.refresh()


window.bye()
window.exitonclick()