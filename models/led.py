from machine import Pin, PWM


class Led:
    """
    TODO Split this into two parts. One for configuration and one for the actual controls
    Configuration for the LED Module
    """
    red_gpio = 0
    green_gpio = 1
    blue_gpio = 2

    r_pin: PWM = None
    g_pin: PWM = None
    b_pin: PWM = None

    def __init__(self, r: int, g: int, b: int):
        """
        Constructor
        """
        self.red_gpio = r
        self.green_gpio = g
        self.blue_gpio = b

    def set_hw_pins(self, r_pin: Pin, g_pin: Pin, b_pin: Pin) -> None:
        """
        Sets the HW Pins used for controlling the LED
        """
        self.r_pin = PWM(r_pin)
        self.g_pin = PWM(g_pin)
        self.b_pin = PWM(b_pin)
        self.r_pin.freq(1000)
        self.g_pin.freq(1000)
        self.b_pin.freq(1000)

    def set_color(self, r_value: int, g_value: int, b_value: int) -> None:
        """
        Sets the color to be displayed on the LED
        """
        self._convert_color_and_set_duty(
            self.r_pin,
            r_value
        )
        self._convert_color_and_set_duty(
            self.g_pin,
            g_value
        )
        self._convert_color_and_set_duty(
            self.b_pin,
            b_value
        )

    def _convert_color_and_set_duty(self, pin: PWM, color_value: int) -> None:
        """
        Converts the color value to the duty cycle number and sets in the given pin
        :param pin: Pin to update
        :param color_value: Color Value to set
        """
        duty_cycle = int((color_value / 255) * 65535)
        pin.duty_u16(duty_cycle)
