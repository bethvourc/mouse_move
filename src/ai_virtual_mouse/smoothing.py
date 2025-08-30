# src/ai_virtual_mouse/smoothing.py

from typing import Tuple


class Smoother:
    """
    Applies exponential moving average (EMA) to cursor coordinates
    to reduce jitter in hand tracking.
    """

    def __init__(self, alpha: float = 0.3):
        """
        alpha: Smoothing factor between 0 (very smooth, very laggy) and 1 (no smoothing)
        """
        self.alpha = alpha
        self.prev_x = None
        self.prev_y = None

    def reset(self):
        """Reset the stored state (e.g., when hand is lost)."""
        self.prev_x = None
        self.prev_y = None

    def smooth(self, x: int, y: int) -> Tuple[int, int]:
        """
        Returns smoothed (x, y) values based on EMA.
        """
        if self.prev_x is None or self.prev_y is None:
            self.prev_x, self.prev_y = x, y
            return x, y

        smooth_x = int(self.alpha * x + (1 - self.alpha) * self.prev_x)
        smooth_y = int(self.alpha * y + (1 - self.alpha) * self.prev_y)

        self.prev_x, self.prev_y = smooth_x, smooth_y
        return smooth_x, smooth_y
