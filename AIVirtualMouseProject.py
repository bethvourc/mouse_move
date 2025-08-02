import cv2
import numpy as np
import pyautogui
from ai_virtual_mouse.camera import Camera


class ColorHandDetector:
    def __init__(self, hsv_lower, hsv_upper):
        self.hsv_lower = hsv_lower
        self.hsv_upper = hsv_upper

    def findHands(self, img, draw: bool = True):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv, self.hsv_lower, self.hsv_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bbox_list = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Reject small blobs/noise
                x, y, w, h = cv2.boundingRect(cnt)
                bbox_list.append((x, y, w, h))
                if draw:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img, bbox_list


def main():
    with Camera(index=0) as cam:
        detector = ColorHandDetector(
            hsv_lower=np.array([36, 25, 25]),
            hsv_upper=np.array([86, 255, 255]),
        )
        w_scr, h_scr = pyautogui.size()
        w_cam, h_cam = cam.resolution

        while True:
            success, img = cam.read()
            if not success:
                continue

            img, bbox_list = detector.findHands(img)

            if bbox_list:
                x, y, w, h = bbox_list[0]
                cx, cy = x + w // 2, y + h // 2

                screen_x = np.interp(cx, (0, w_cam), (0, w_scr))
                screen_y = np.interp(cy, (0, h_cam), (0, h_scr))
                pyautogui.moveTo(screen_x, screen_y)

                if w * h < 25_000:
                    pyautogui.click()

            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
