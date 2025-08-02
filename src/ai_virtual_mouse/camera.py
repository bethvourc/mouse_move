"""
ai_virtual_mouse.camera
Lightweight wrapper around cv2 VideoCapture for easier testing and
future multi-camera or video-file input.

Usage:
    from ai_virtual_mouse.camera import Camera
    with Camera(index=0) as cam:
        ok, frame = cam.read()
"""

from __future__ import annotations

from typing import Tuple

import cv2


class Camera:
    """Encapsulates cv2.VideoCapture plus a few utility helpers."""

    def __init__(
        self, index: int = 0, width: int | None = None, height: int | None = None
    ) -> None:
        self._cap = cv2.VideoCapture(index)
        if width is not None:
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height is not None:
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self._cap.isOpened():
            raise RuntimeError(f"Could not open camera at index {index}")

    # -- context-manager helpers --
    def __enter__(self) -> "Camera":  # noqa: D401
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: D401
        self.release()

    # -- facade methods around cv2 methods we actually use --
    def read(self):
        """Return (success, frame) exactly like cv2.VideoCapture.read()."""
        return self._cap.read()

    def release(self) -> None:
        self._cap.release()

    # -- convenience helpers --
    @property
    def resolution(self) -> Tuple[int, int]:
        """Return (width, height) of current camera feed in pixels."""
        width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height
