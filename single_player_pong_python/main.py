import atexit
import time
import turtle
from enum import Enum
from typing import Callable


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
    paddle.direction = Direction.NO_DIRECTION
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


def setup_keypress(
    win: turtle.TurtleScreen,
    current_direction: Callable[[], Direction],
    update_direction: Callable[[Direction], None],
):
    win.listen()
    win.onkeypress(
        lambda: update_direction(right_pressed(current_direction())), "Right"
    )
    win.onkeyrelease(
        lambda: update_direction(right_released(current_direction())), "Right"
    )
    win.onkeypress(lambda: update_direction(left_pressed(current_direction())), "Left")
    win.onkeyrelease(
        lambda: update_direction(left_released(current_direction())), "Left"
    )


def setup_window():
    win = turtle.Screen()
    win.title("Test game")
    win.bgcolor("black")
    win.setup(width=800, height=600)
    win.tracer(0)
    win.cv._rootwindow.resizable(False, False)
    return win


def start_game():
    win = setup_window()

    paddle = create_paddle()
    paddle_dir = Direction.NO_DIRECTION

    def update_direction(direction: Direction):
        nonlocal paddle_dir
        paddle_dir = direction

    def current_direction():
        nonlocal paddle_dir
        return paddle_dir

    setup_keypress(win, current_direction, update_direction)

    running = True

    def exit_game():
        nonlocal running
        running = False
        print("Bye")

    atexit.register(exit_game)

    last_frame_time: float = 0
    fps = 30

    while running:
        current_time = time.time()
        delta_time = current_time - last_frame_time
        last_frame_time = current_time
        sleep_time = 1.0 / fps - delta_time
        if sleep_time > 0:
            time.sleep(sleep_time)
        if running:
            handle_direction(paddle, paddle_dir, delta_time)
            win.update()

    win.bye()


start_game()
