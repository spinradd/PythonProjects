from turtle import Screen, Turtle
from snake_class import Snake
from food_class import Food
from scoreboard_class import Scoreboard
from border_class import Border
from starting_sequence import Start_Class
import time

#set up screen
screen = Screen()
screen.setup(width=600, height=500)
screen.title("Snake!")
screen.colormode(255)
screen.bgcolor("black")
screen.tracer(False)

#initialize classes
border = Border() #create border
board = Scoreboard() #create score board visuals
start = Start_Class() #create keyboard visual
start.create_keyboard()

display = Start_Class() #create countdown
display.display_sequence()

snake = Snake()
food = Food()

#begin event listening
screen.listen()
screen.onkey(snake.up, "w")
screen.onkey(snake.down, "s")
screen.onkey(snake.left, "a")
screen.onkey(snake.right, "d")
screen.onkey(screen.bye, "Escape")

# while user wants to play...
keep_playing = True
while keep_playing:

    # assume game is not over
    game_is_over = False

    # while snake has not hit itself or wall
    while not game_is_over:
        screen.update()
        snake.move()
        time.sleep(.1)

        # if snake hits food, move food, update snake and score visuals
        if snake.snake_head.distance(food) < 15:
            food.move_food(snake.body)
            snake.extend()
            board.score += 1
            board.refresh()
        # if snake hits border, end game, end loop
        if border.is_border_breached(snake.snake_head):
            game_is_over = True
            continue
        # if snake hits itself, end game, end loop
        if snake.snake_collision():
            game_is_over = True
            continue

    # Once game is over, erase snake and food from screen
    # initiate game_over sequence, initiate
    snake.delete_snake()
    food.delete_food()
    board.game_over()
    time.sleep(3)

    # prompt user and ask if they want to keep playing
    board.continue_snake()
    board.update_high_score()

    # if user wants to stop, end loop, else reset game
    if not board.continue_game:
        keep_playing = False
    else:
        board.continue_countdown()
        board.score = 0
        board.refresh()
        snake.refresh()
        food.refresh()
        screen.listen()

board.thanks_for_playing()
screen.bye()

