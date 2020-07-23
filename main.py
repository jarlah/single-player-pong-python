import turtle
import time
from enum import Enum


class Direction(Enum):
    NO_DIRECTION = 0
    LEFT = 1
    RIGHT = 2


def create_paddle() -> turtle.Turtle:
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.color("white")
    paddle.shape("square")
    paddle.shapesize(stretch_wid=1, stretch_len=5)
    paddle.penup()
    paddle.goto(0, -250)
    paddle.dir = Direction.NO_DIRECTION
    return paddle


def right_pressed(paddle: turtle.Turtle):
    if paddle.dir == Direction.NO_DIRECTION:
        paddle.dir = Direction.RIGHT


def right_released(paddle: turtle.Turtle):
    if paddle.dir == Direction.RIGHT:
        paddle.dir = Direction.NO_DIRECTION


def left_pressed(paddle: turtle.Turtle):
    if paddle.dir == Direction.NO_DIRECTION:
        paddle.dir = Direction.LEFT


def left_released(paddle: turtle.Turtle):
    if paddle.dir == Direction.LEFT:
        paddle.dir = Direction.NO_DIRECTION


def move_left(dt, paddle: turtle.Turtle):
    x = paddle.xcor()
    x -= 200 * dt
    paddle.setx(x)
    return paddle


def move_right(dt, paddle: turtle.Turtle):
    x = paddle.xcor()
    x += 200 * dt
    paddle.setx(x)
    return paddle


def handle_direction(paddle, dt: float):
    switcher = {
        Direction.RIGHT: lambda: move_right(dt, paddle),
        Direction.LEFT: lambda: move_left(dt, paddle),
    }
    func = switcher.get(paddle.dir, lambda: paddle)
    return func()


def setup_keypress(win, paddle):
    win.listen()
    win.onkeypress(lambda: right_pressed(paddle), "Right")
    win.onkeyrelease(lambda: right_released(paddle), "Right")
    win.onkeypress(lambda: left_pressed(paddle), "Left")
    win.onkeyrelease(lambda: left_released(paddle), "Left")


def setup_window():
    win = turtle.Screen()
    win.title("Test game")
    win.bgcolor("black")
    win.setup(width=800, height=600)
    win.tracer(0)
    return win


def start():
    win = setup_window()
    paddle = create_paddle()
    setup_keypress(win, paddle)
    running = True
    last_frame_time: float = 0
    fps = 30
    while running:
        current_time = time.time()
        delta_time = current_time - last_frame_time
        last_frame_time = current_time
        sleep_time = 1. / fps - delta_time
        if sleep_time > 0:
            time.sleep(sleep_time)
        handle_direction(paddle, delta_time)
        win.update()


start()
