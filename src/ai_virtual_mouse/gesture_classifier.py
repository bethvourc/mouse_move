# src/ai_virtual_mouse/gesture_classifier.py

from typing import List, Literal

from .gestures import distance, fingers_up

Gesture = Literal["left_click", "right_click", "scroll_up", "scroll_down", "none"]


class GestureClassifier:
    def __init__(
        self,
        click_threshold: float = 40.0,
        scroll_threshold: float = 40.0,
        finger_spacing_threshold: float = 30.0,
    ):
        self.click_threshold = click_threshold
        self.scroll_threshold = scroll_threshold
        self.finger_spacing_threshold = finger_spacing_threshold

    def classify(self, landmarks: List[tuple[int, int, int]]) -> Gesture:
        if not landmarks or len(landmarks) < 21:
            return "none"

        up = fingers_up(landmarks)

        thumb_tip = landmarks[4][1:3]
        index_tip = landmarks[8][1:3]
        middle_tip = landmarks[12][1:3]

        thumb_index_dist = distance(thumb_tip, index_tip)
        index_middle_dist = distance(index_tip, middle_tip)

        # Left Click: Thumb + Index close together, rest down
        if (
            up[0]
            and up[1]
            and not any(up[2:])
            and thumb_index_dist < self.click_threshold
        ):
            return "left_click"

        # Right Click: Index + Middle up and close
        if (
            up[1]
            and up[2]
            and not any(up[3:])
            and index_middle_dist < self.click_threshold
        ):
            return "right_click"

        # Scroll Up: Only Index up
        if up == [False, True, False, False, False]:
            return "scroll_up"

        # Scroll Down: Only Middle up
        if up == [False, False, True, False, False]:
            return "scroll_down"

        return "none"
