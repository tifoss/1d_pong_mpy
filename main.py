"""
1D Pong
"""
import random
from microbit import pin0, pin1, pin2, sleep, button_a, button_b
from neopixel import NeoPixel

# Stubs miss the self parameter.
# pylint: disable=too-many-function-args
# We do embedded, global state is ok.
# pylint: disable=global-statement

BACKGRUND_COLOR = (50, 0, 0)
BALL_COLOR = (255, 255, 255)
P1_COLOR = (255, 255, 0)
P2_COLOR = (0, 0, 255)
HIT_COLOR = (255, 0, 0)
HIT_AREA = (0, 255, 0)
HIT_AREA_SIZE = 5
PIXEL_COUNT = 40
DEFAULT_SPEED = 10
HIT_TIME = 250
MAX_SCORE = 5

PLAYGROUND = NeoPixel(pin0, PIXEL_COUNT)
P1_SCORE = 0
P2_SCORE = 0
BALL = 0
STEP = 0
SPEED = DEFAULT_SPEED


def prepare_playground():
    """
    Fill pixels with playground.
    """
    PLAYGROUND.fill(BACKGRUND_COLOR)

    for i in range(0, HIT_AREA_SIZE):
        PLAYGROUND[i] = HIT_AREA
    for i in range((PIXEL_COUNT - HIT_AREA_SIZE), PIXEL_COUNT):
        PLAYGROUND[i] = HIT_AREA

    mid = int((PIXEL_COUNT / 2) + 1)
    for i in range((mid - P1_SCORE), mid):
        PLAYGROUND[i] = P1_COLOR

    for i in range(mid, (mid + P2_SCORE)):
        PLAYGROUND[i] = P2_COLOR


def init_playground():
    """
    Update pixels to show the playground.
    """
    prepare_playground()
    PLAYGROUND.write()


def draw_ball():
    """
    Draw ball.
    """
    prepare_playground()
    if 0 <= BALL and BALL < PIXEL_COUNT:
        PLAYGROUND[BALL] = BALL_COLOR
        PLAYGROUND.write()


def draw_hit():
    """
    Draw hit.
    """
    prepare_playground()
    if 0 <= BALL and BALL < PIXEL_COUNT:
        PLAYGROUND[BALL] = HIT_COLOR
        PLAYGROUND.write()
        sleep(HIT_TIME)


def init_buttons():
    """
    Init the push buttons.
    """
    pin1.write_analog(1023)
    pin2.write_analog(1023)


def select_player():
    """
    Decide which player starts the game.
    """
    global BALL, STEP

    if button_a.was_pressed():
        BALL = 0
        STEP = 1
        return True
    if button_b.was_pressed():
        BALL = PIXEL_COUNT - 1
        STEP = -1
        return True
    return False


def p1_fire():
    """
    Player 1 pressed the fire button.
    """
    global STEP, SPEED

    draw_hit()

    if 0 <= BALL and BALL < HIT_AREA_SIZE:
        STEP = 1
        SPEED = STEP * 5
    else:
        p2_score()


def p1_score():
    """
    Player 1 get a point.
    """
    global P1_SCORE, STEP, BALL, SPEED

    P1_SCORE += 1
    STEP = 1

    if BALL >= HIT_AREA_SIZE or BALL < 0:
        BALL = 0
        SPEED = DEFAULT_SPEED

    draw_ball()

    pin1.write_analog(1023)
    pin2.write_analog(0)

    # Wait for player 1 to fire.
    if P1_SCORE < MAX_SCORE:
        while True:
            if button_a.was_pressed():
                break
            sleep(DEFAULT_SPEED)


def p2_fire():
    """
    Player 2 pressed the fire button.
    """
    global STEP, SPEED

    draw_hit()

    if (PIXEL_COUNT - HIT_AREA_SIZE) <= BALL and BALL < PIXEL_COUNT:
        STEP = -1
        SPEED = (PIXEL_COUNT - 1 - BALL) * 5
    else:
        p1_score()


def p2_score():
    """
    Player 1 get a point.
    """
    global P2_SCORE, STEP, BALL, SPEED

    P2_SCORE += 1
    STEP = -1

    if BALL < (PIXEL_COUNT - HIT_AREA_SIZE) or BALL > PIXEL_COUNT:
        BALL = PIXEL_COUNT - 1
        SPEED = DEFAULT_SPEED

    draw_ball()

    pin1.write_analog(0)
    pin2.write_analog(1023)

    # Wait for player 1 to fire.
    if P2_SCORE < MAX_SCORE:
        while True:
            if button_b.was_pressed():
                break
            sleep(DEFAULT_SPEED)


def check_win():
    """
    Check if a player has won the game.
    """
    if P1_SCORE >= MAX_SCORE or P2_SCORE >= MAX_SCORE:
        win()
        return True


def reset_buttons():
    """
    Reset button pressed state.
    """
    button_a.was_pressed()
    button_b.was_pressed()


def game_loop():
    """
    Main game loop.
    """
    global P1_SCORE, P2_SCORE, BALL, STEP, SPEED

    P1_SCORE = 0
    P2_SCORE = 0
    BALL = 0
    STEP = 0
    SPEED = DEFAULT_SPEED

    init_playground()

    while True:
        if select_player():
            break
        sleep(DEFAULT_SPEED)

    reset_buttons()

    if STEP > 0:
        pin1.write_analog(1023)
        pin2.write_analog(0)
    else:
        pin1.write_analog(0)
        pin2.write_analog(1023)

    while True:
        if button_a.was_pressed():
            p1_fire()
            reset_buttons()

        if button_b.was_pressed():
            p2_fire()
            reset_buttons()

        if check_win():
            break

        draw_ball()

        sleep(SPEED)

        BALL += STEP
        if BALL >= PIXEL_COUNT:
            p1_score()
            reset_buttons()
        elif BALL < 0:
            p2_score()
            reset_buttons()

        if check_win():
            break


def win():
    """
    Display win animation.
    """
    global P1_SCORE, P2_SCORE

    start = 0
    end = int(PIXEL_COUNT / 2)
    if P2_SCORE == MAX_SCORE:
        start = end
        end = PIXEL_COUNT - 1

    P1_SCORE = 0
    P2_SCORE = 0

    for i in range(0, 200):
        for i in range(start, end):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            PLAYGROUND[i] = (r, g, b)
        PLAYGROUND.write()
        sleep(DEFAULT_SPEED)

    init_buttons()
    init_playground()


def main():
    """
    Game main function.
    """
    while True:
        init_buttons()
        init_playground()
        game_loop()


main()
