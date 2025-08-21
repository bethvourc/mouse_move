# src/ai_virtual_mouse/mouse_controller.py

from typing import Tuple

import pyautogui


class MouseController:
    """
    Wraps pyautogui to abstract away direct OS interaction for mouse control.
    Useful for testing, mocking, or later swapping with platform-specific backends.
    """

    def __init__(self, screen_size: Tuple[int, int] | None = None):
        self.screen_width, self.screen_height = screen_size or pyautogui.size()

    def move_to(self, x: int, y: int, duration: float = 0.0) -> None:
        """Move cursor to (x, y) with optional duration."""
        pyautogui.moveTo(x, y, duration=duration)

    def click(self) -> None:
        """Perform a left-click."""
        pyautogui.click()

    def right_click(self) -> None:
        """Perform a right-click."""
        pyautogui.rightClick()

    def scroll(self, amount: int) -> None:
        """
        Scroll vertically. Positive = up, Negative = down.
        `amount` is in units, not pixels.
        """
        pyautogui.scroll(amount)

    def get_screen_size(self) -> Tuple[int, int]:
        return self.screen_width, self.screen_height

    def normalize_coords(
        self, x: int, y: int, frame_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """
        Converts camera-space coordinates to screen-space.
        Assumes frame_size is (width, height) of camera input.
        """
        frame_w, frame_h = frame_size
        screen_x = int((x / frame_w) * self.screen_width)
        screen_y = int((y / frame_h) * self.screen_height)
        return screen_x, screen_y
