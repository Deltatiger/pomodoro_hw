from models.button import Button
from machine import Timer
import constants
import utime


class TimerManager:
    """
    Manager class for the Timer Functionality
    """

    _buttons: list[Button] = []
    _timer: Timer | None = None
    _time_remaining_in_ms = 0
    _last_run_time = 0

    def __init__(self, buttons: list[Button]):
        """
        Constructor
        :param buttons: List of supported Buttons
        :poram time_display: Time Display Control
        """
        self._buttons = buttons

    def update_timer(self):
        """
        Updates the timer based on if anything was clicked
        """
        pressed_button = self._update_and_get_pressed_button()
        # Create new timer based on the clicked button
        if pressed_button is None:
            return
        # Update the Display on the timer
        self._start_timer_for_button(pressed_button)

    def get_time_remaining(self) -> int:
        """
        Gets the Time Remaining based on the running timer or 0 if no timer is running
        """
        if self._timer is None:
            return 0
        return self._time_remaining_in_ms

    def _update_and_get_pressed_button(self) -> Button | None:
        """
        Updates the status of the buttons and gets the currently pressed button (first)
        :returns: Pressed Button or None
        """
        for button in self._buttons:
            button.update_pressed_status()
        # TODO Handle combination click for some special actions if required.
        for button in self._buttons:
            if button.is_pressed:
                return button
        return None

    def _start_timer_for_button(self, pressed_button: Button) -> None:
        """
        Starts the timer for the Button that has been pressed
        :param pressed_button: Button that was pressed
        """
        # Destroy the old timer
        if self._timer is not None:
            self._timer.deinit()
            self._timer = None
        # Reset the time remaining
        self._time_remaining_in_ms = pressed_button.time * constants.MINUTE_IN_MS
        self._last_run_time = utime.ticks_ms()
        # Create the new timer
        self._timer = Timer()
        self._timer.init(
            mode=Timer.PERIODIC,
            period=constants.TIMER_PERIOD,
            callback=self._handle_time_update
        )

    def _handle_time_update(self, timer: Timer) -> None:
        """
        Handles the update to the time remaining
        """
        diff = utime.ticks_diff(
            utime.ticks_ms(),
            self._last_run_time
        )
        self._last_run_time = utime.ticks_ms()
        self._time_remaining_in_ms = self._time_remaining_in_ms - diff