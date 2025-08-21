from machine import Pin


class Button:
    """
    Button class definition
    """
    gpio = 0
    action = None
    time = None
    hw_pin: Pin = None
    is_pressed = False

    def __init__(self, gpio: int, action: str, time: int):
        """
        Constructor
        """
        self.gpio = gpio
        self.action = action
        self.time = time

    def update_pressed_status(self) -> None:
        """
        Checks and updates the pressed status of the Button
        """
        if self.hw_pin is None:
            raise EnvironmentError('HW Pin not set.')
        self.is_pressed = self.hw_pin.value() == 1
