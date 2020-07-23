import turtle
import time
from enum import Enum
from typing import AnyStr, Callable


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


def right_pressed(paddle_dir: Direction):
    if paddle_dir == Direction.NO_DIRECTION:
        paddle_dir = Direction.RIGHT
    return paddle_dir


def right_released(paddle_dir: Direction):
    if paddle_dir == Direction.RIGHT:
        paddle_dir = Direction.NO_DIRECTION
    return paddle_dir


def left_pressed(paddle_dir: Direction):
    if paddle_dir == Direction.NO_DIRECTION:
        paddle_dir = Direction.LEFT
    return paddle_dir


def left_released(paddle_dir: Direction):
    if paddle_dir == Direction.LEFT:
        paddle_dir = Direction.NO_DIRECTION
    return paddle_dir


def move_left(dt: float, paddle: turtle.Turtle):
    x = paddle.xcor()
    x -= 200 * dt
    paddle.setx(x)
    return paddle


def move_right(dt: float, paddle: turtle.Turtle):
    x = paddle.xcor()
    x += 200 * dt
    paddle.setx(x)
    return paddle


def handle_direction(paddle: turtle.Turtle, direction: Direction, dt: float):
    switcher = {
        Direction.RIGHT: lambda: move_right(dt, paddle),
        Direction.LEFT: lambda: move_left(dt, paddle),
    }
    func = switcher.get(direction, lambda: paddle)
    return func()


def setup_keypress(win: turtle.TurtleScreen, direction: Direction, direction_updater: Callable[[Direction], None]):
    win.listen()
    win.onkeypress(lambda: direction_updater(right_pressed(direction)), "Right")
    win.onkeyrelease(lambda: direction_updater(right_released(direction)), "Right")
    win.onkeypress(lambda: direction_updater(left_pressed(direction)), "Left")
    win.onkeyrelease(lambda: direction_updater(left_released(direction)), "Left")


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
    paddle_dir = Direction.NO_DIRECTION

    def dir_update(direction: Direction):
        nonlocal paddle_dir
        paddle_dir = direction

    setup_keypress(win, paddle_dir, dir_update)
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
        handle_direction(paddle, paddle_dir, delta_time)
        win.update()


start()
