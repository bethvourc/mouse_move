# src/ai_virtual_mouse/hand_tracker.py

import cv2
import mediapipe as mp


class HandTracker:
    def __init__(
        self,
        static_mode=False,
        max_hands=2,
        detection_confidence=0.7,
        tracking_confidence=0.6,
    ):
        self.static_mode = static_mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.static_mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, image, draw=True):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        image, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )

        return image

    def get_landmark_positions(self, image, hand_index=0):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            try:
                hand = self.results.multi_hand_landmarks[hand_index]
                for id, lm in enumerate(hand.landmark):
                    h, w, _ = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmark_list.append((id, cx, cy))
            except IndexError:
                pass
        return landmark_list
