import json
import constants
from models.button import Button
from models.display import Display


class Configuration:
    """
    Configuration Reading and Management
    """

    buttons: list[Button] = []
    display: Display = None
    
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
