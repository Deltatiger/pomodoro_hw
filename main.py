from configuration import Configuration
from machine import Pin, Timer
from network_manager import NetworkManager
from tm1637 import TM1637
from time import sleep
from timer_manager import TimerManager

config = Configuration()
blink_phase = False


def convert_to_time_str(time_remaining: int) -> str:
    """
    Convert the number to a time string
    :param time_remaining: Time remaining in ms
    :returns: Time string
    """
    time_remaining = abs(time_remaining)  # Fix the loop around
    minutes_left = int(time_remaining / 60 / 1000)
    seconds_left = int(time_remaining / 1000) % 60
    display_string = ("%02d" % minutes_left) + ("%02d" % seconds_left)
    return display_string


def display_time(time_remaining: int, time_display: TM1637) -> None:
    """
    Display the time
    :param time_remaining: Time Remaining in ms
    :param time_display: Display Controller for the Time
    """

    if time_remaining == 0:
        time_display.brightness(1)
        time_display.show("DONE")
        return
    global blink_phase
    time_string = convert_to_time_str(time_remaining)
    time_display.brightness(5)
    if time_remaining < 0:
        # Need to blink the time
        if blink_phase:
            time_display.show('    ')
        else:
            time_display.show(time_string)
        blink_phase = not blink_phase
    else:
        time_display.show(time_string)


# Configure the buttons
for button in config.buttons:
    hw_button = Pin(
        button.gpio,
        Pin.IN,
        Pin.PULL_DOWN
    )
    button.hw_pin = hw_button

# Configure the Display
config.display.hw_controller = TM1637(
    clk=Pin(config.display.clock_pin),
    dio=Pin(config.display.data_pin)
)

config.network.led.set_hw_pins(
    r_pin=Pin(config.network.led.red_gpio, Pin.OUT),
    g_pin=Pin(config.network.led.green_gpio, Pin.OUT),
    b_pin=Pin(config.network.led.blue_gpio, Pin.OUT)
)

network_manager = NetworkManager(config.network)
network_manager.connect()
connected_status = False
while not connected_status:
    # TODO Have a counter so that this doesn't go on forever
    connected_status = network_manager.check_connection_status()

print("Connected to the Network")

timer_manager = TimerManager(config.buttons)

while True:
    timer_manager.update_timer()
    display_time(
        timer_manager.get_time_remaining(),
        config.display.hw_controller
    )
    sleep(0.250)
