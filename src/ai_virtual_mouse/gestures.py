# src/ai_virtual_mouse/gestures.py

from math import hypot
from typing import List, Tuple

# Define fingertip landmark indices from MediaPipe Hands
FINGER_TIPS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky


def get_finger_tips(landmarks: List[Tuple[int, int, int]]) -> dict:
    """
    Returns a dict of fingertip positions: {index: (x, y)}.
    """
    return {idx: (x, y) for (i, x, y) in landmarks if i in FINGER_TIPS for idx in [i]}


def fingers_up(landmarks: List[Tuple[int, int, int]]) -> List[bool]:
    """
    Determines which fingers are up based on y-coordinate comparison with lower joints.
    Returns: List[bool] in order: [thumb, index, middle, ring, pinky]
    """
    fingers = []

    if not landmarks or len(landmarks) < 21:
        return [False] * 5

    # Thumb: compare x because it's horizontal
    fingers.append(landmarks[4][1] > landmarks[3][1])

    # Other fingers: compare y
    fingers.append(landmarks[8][2] < landmarks[6][2])  # Index
    fingers.append(landmarks[12][2] < landmarks[10][2])  # Middle
    fingers.append(landmarks[16][2] < landmarks[14][2])  # Ring
    fingers.append(landmarks[20][2] < landmarks[18][2])  # Pinky

    return fingers


def distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """
    Euclidean distance between two points.
    """
    return hypot(p2[0] - p1[0], p2[1] - p1[1])
