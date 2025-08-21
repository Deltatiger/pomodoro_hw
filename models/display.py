from tm1637 import TM1637


class Display:
    """
    Model that ha
    """
    clock_pin = 0
    data_pin = 0
    hw_controller: TM1637 = None

    def __init__(self, data_pin: int, clock_pin: int) -> None:
        """
        Constructor
        """
        self.clock_pin = clock_pin
        self.data_pin = data_pin

    def set_controller(self, controller: TM1637):
        """
        Sets a reference to the Controller
        """
        self.hw_controller = controller
