# src/ai_virtual_mouse/threading.py

from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable, Optional


class FrameProcessor:
    """
    Wraps any frame-processing function in a background thread using ThreadPoolExecutor.
    Useful for offloading inference while keeping the main UI loop responsive.
    """

    def __init__(self, process_fn: Callable, max_workers: int = 1):
        """
        process_fn: Callable that takes a frame and returns results (e.g., landmarks, gestures)
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.process_fn = process_fn
        self.future: Optional[Future] = None

    def submit(self, frame):
        """
        Submit a frame to be processed. Non-blocking.
        """
        if self.future is None or self.future.done():
            self.future = self.executor.submit(self.process_fn, frame.copy())

    def result(self):
        """
        Returns the result of the last processed frame (if available).
        """
        if self.future and self.future.done():
            return self.future.result()
        return None

    def shutdown(self):
        """
        Cleanly shutdown the background thread.
        """
        self.executor.shutdown(wait=True)
