import tm1637
from machine import Pin, Timer
from utime import sleep
my_display = tm1637.TM1637(clk=Pin(1), dio=Pin(0))
short_timer_button = Pin(15, Pin.IN, Pin.PULL_DOWN)
long_timer_button = Pin(14, Pin.IN, Pin.PULL_DOWN)

is_short_timer_clicked = False
is_long_timer_clicked = False

timer = None
time_remaining_in_ms = 0

my_display.brightness(6)

def update_button_states():
    """
    Updates the button click status based on the readings
    """
    global is_short_timer_clicked, is_long_timer_clicked
    is_short_timer_clicked = short_timer_button.value() == 1
    is_long_timer_clicked = long_timer_button.value() == 1
    
    if is_short_timer_clicked:
        print("Button Short clicked")
    if is_long_timer_clicked:
        print("Button Long clicked")

def update_time_remaining(timer_ref):
    """
    Call back to handle the updation of the time based on the period
    """
    global time_remaining_in_ms
    time_remaining_in_ms = time_remaining_in_ms - 500
    
    if time_remaining_in_ms <= 0:
        timer_ref.deinit()
        timer_ref = None
        time_remaining_in_ms = 0
    
def reset_timer_based_on_click():
    """
    Sets the timer based on the buttons that were clicked
    """
    global is_short_timer_clicked, is_long_timer_clicked, timer, time_remaining_in_ms
    duration = 0
    if is_short_timer_clicked:
        duration = 15
    if is_long_timer_clicked:
        duration = 40
    if duration == 0:
        # Nothing was clicked. Don't do anything.
        return
    
    time_remaining_in_ms = duration * 60 * 1000 # Conversion to ms
    
    if timer is not None:
        timer.deinit()
        timer = None
    timer = machine.Timer()
    timer.init(mode=Timer.PERIODIC, period=500, callback=update_time_remaining)

def display_time():
    """
    Displays the time based on the time remaining or the message.
    """
    global my_display, time_remaining_in_ms
    
    if time_remaining_in_ms == 0:
        my_display.brightness(1)
        my_display.show("DONE")
    else:
        minutes_left = int(time_remaining_in_ms / 60 / 1000)
        seconds_left = int(time_remaining_in_ms / 1000) % 60
        display_string = ("%02d" % minutes_left) + ("%02d" % seconds_left)
        my_display.brightness(5)
        my_display.show(display_string)

while True:
    update_button_states()
    reset_timer_based_on_click()
    display_time()
    sleep(0.5)

print("Stopped")
