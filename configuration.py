import json
import constants
from models.button import Button
from models.display import Display
from models.network import Network
from models.led import Led


class Configuration:
    """
    Configuration Reading and Management
    """

    buttons: list[Button] = []
    display: Display = None
    network: Network = None
    
    def __init__(self):
        """
        Constructor
        """
        json_data = self._read_config_file()
        if json_data is None:
            # Nothing to process. Ignore.
            return
        self._set_button_config(json_data)
        self._set_display_config(json_data)
        self._set_network_config(json_data)

    def _read_config_file(self) -> dict | None:
        """
        Reads the configuration file and updates the Configuration
        """
        try:
            with open(constants.CONFIG_FILE_NAME, 'r') as fp:
                return json.load(fp)
        except:
            return None

    def _set_button_config(self, json_data) -> None:
        """
        Sets the button data from the JSON Configuration
        """
        if 'buttons' not in json_data:
            return

        for button_data in json_data['buttons']:
            button_item = Button(
                button_data['gpio'],
                button_data['action'],
                button_data['time']
            )
            self.buttons.append(button_item)

    def _set_display_config(self, json_data: dict) -> None:
        """
        Sets the configuration required for running the Display
        :param json_data: Json Configuration File
        """
        if 'display' not in json_data:
            return

        display_config = json_data['display']
        self.display = Display(
            clock_pin=display_config['clock_gpio'],
            data_pin=display_config['data_gpio']
        )

    def _set_network_config(self, json_data: dict) -> None:
        """
        Sets the Network Configuration
        :param json_data: Json Configuration Data
        """
        networking_config = json_data['network']
        if networking_config is None:
            pass
        self.network = Network()
        self.network.ssid = networking_config['ssid']
        self.network.password = networking_config['password']
        # Read the color LED control notification.
        led_controls = networking_config['led_module_inputs']
        self.network.led = Led(
            r=led_controls['r_gpio'],
            g=led_controls['g_gpio'],
            b=led_controls['b_gpio']
        )
