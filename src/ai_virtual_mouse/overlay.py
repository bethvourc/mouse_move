# src/ai_virtual_mouse/overlay.py

from typing import Optional

import cv2


def draw_label(
    image,
    label: str,
    position: tuple[int, int] = (10, 40),
    color: tuple[int, int, int] = (0, 255, 0),
    font_scale: float = 0.9,
    thickness: int = 2,
) -> None:
    """
    Draws a label on the frame at the given position.
    """
    cv2.putText(
        image,
        label,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
        lineType=cv2.LINE_AA,
    )


def draw_debug_info(
    image,
    gesture: Optional[str] = None,
    fps: Optional[float] = None,
    roi: Optional[dict] = None,
) -> None:
    """
    Draws debug overlays: gesture label, FPS, region-of-interest (if any).
    """
    y = 40
    if gesture:
        draw_label(image, f"Gesture: {gesture}", position=(10, y))
        y += 30

    if fps is not None:
        draw_label(image, f"FPS: {fps:.2f}", position=(10, y), color=(255, 255, 0))
        y += 30

    if roi and roi.get("enabled"):
        h, w, _ = image.shape
        x_min = int(roi["x_min"] * w)
        x_max = int(roi["x_max"] * w)
        y_min = int(roi["y_min"] * h)
        y_max = int(roi["y_max"] * h)
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 255), 2)
        draw_label(image, "ROI", position=(x_min + 5, y_min - 10), color=(255, 0, 255))
