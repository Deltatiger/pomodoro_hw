import constants
from configuration import Configuration
from models.button import Button
from machine import Pin, Timer
import tm1637

config = Configuration()

time_remaining_in_ms = 0
timer: Timer | None = None


def get_pressed_button(buttons: list[Button]) -> Button | None:
    """
    Finds the first button that is pressed
    :param buttons: List of buttons
    :returns: First pressed button or None
    """
    if buttons is None:
        return None
    for button in buttons:
        if button.is_pressed:
            return button
    return None


def update_time_remaining(timer_ref: Timer) -> None:
    """
    Updates the time remaining
    """
    global time_remaining_in_ms
    time_remaining_in_ms = time_remaining_in_ms - constants.TIMER_PERIOD


def update_timer_based_on_click(pressed_button: Button) -> None:
    """
    Updates the remaining timer based on the pressed button
    :param pressed_button: Currently pressed button
    """
    # Stop the existing timer
    global timer, time_remaining_in_ms
    if timer is not None:
        timer.deinit()
        timer = None
    time_remaining_in_ms = pressed_button.time * constants.MINUTE_IN_MS
    timer = Timer()
    timer.init(
        mode=Timer.PERIODIC,
        period=constants.TIMER_PERIOD,
        callback=update_time_remaining
    )


def display_time() -> None:
    """
    Display the time
    """
    global config, time_remaining_in_ms

    if time_remaining_in_ms == 0:
        config.display.hw_controller.brightness(1)
        config.display.hw_controller.show("DONE")
    else:
        minutes_left = int(time_remaining_in_ms / 60 / 1000)
        seconds_left = int(time_remaining_in_ms / 1000) % 60
        display_string = ("%02d" % minutes_left) + ("%02d" % seconds_left)
        config.display.hw_controller.brightness(5)
        config.display.hw_controller.show(display_string)


# Configure the buttons
for button in config.buttons:
    hw_button = Pin(
        button.gpio,
        Pin.IN,
        Pin.PULL_DOWN
    )
    button.hw_pin = hw_button

# Configure the Display
config.display.hw_controller = tm1637.TM1637(
    clk=Pin(config.display.clock_pin),
    dio=Pin(config.display.data_pin)
)

while True:
    for button in config.buttons:
        button.update_pressed_status()
    pressed_button = get_pressed_button(config.buttons)
    if pressed_button is not None:
        update_timer_based_on_click(pressed_button)
    display_time()

