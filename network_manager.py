import network
from models.network import Network
from models.led import Led


class NetworkManager:
    """
    Managers everything related to the Network
    """

    _network: Network = None
    _station: network.WLAN = None
    _connection_status = False

    def __init__(self, network_config: Network) -> None:
        """
        Constructor
        :param network_config: Network configuration data
        """
        self._network = network_config
        self._network.led.set_color(255, 0, 0)

    def connect(self) -> bool:
        """
        Connects to the configured connection
        """
        if self._network is None:
            return False
        self._station = network.WLAN(
            network.STA_IF
        )
        self._station.active(True)
        self._station.connect(
            self._network.ssid,
            self._network.password
        )
        return True

    def check_connection_status(self) -> bool:
        """
        Checks and returns the connection status
        :returns: Flag representing the connection status
        """
        self._connection_status = False
        if self._station is None:
            # Throw an error
            return False
        self._connection_status = self._station.isconnected()
        # Update the color based on the status
        self._update_led_color()
        return self._connection_status

    def _update_led_color(self):
        """
        Updates the color of the LED based on the connection status
        """
        if self._connection_status:
            self._network.led.set_color(0, 255, 0)
        else:
            self._network.led.set_color(255, 0, 0)
