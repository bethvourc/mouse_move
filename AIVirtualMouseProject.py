import cv2
import numpy as np
import pyautogui

class ColorHandDetector:
    def __init__(self, hsv_lower, hsv_upper):
        self.hsv_lower = hsv_lower
        self.hsv_upper = hsv_upper

    def findHands(self, img, draw=True):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, self.hsv_lower, self.hsv_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bboxList = []
        if contours:
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:  # Minimum area to consider
                    x, y, w, h = cv2.boundingRect(cnt)
                    bboxList.append((x, y, w, h))
                    if draw:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img, bboxList

def main():
    cap = cv2.VideoCapture(0)  # Adjust as per your webcam setup
    detector = ColorHandDetector(hsv_lower=np.array([36, 25, 25]), hsv_upper=np.array([86, 255, 255]))
    wScr, hScr = pyautogui.size()

    while True:
        success, img = cap.read()
        img, bboxList = detector.findHands(img)

        if bboxList:
            # For simplicity, just use the first bounding box
            x, y, w, h = bboxList[0]
            # Calculate the center of the bounding box
            cx, cy = x + w // 2, y + h // 2

            # Convert coordinates to screen size
            screenX = np.interp(cx, (0, 640), (0, wScr))
            screenY = np.interp(cy, (0, 480), (0, hScr))
            pyautogui.moveTo(screenX, screenY)

            # Simple click mechanism: click if the bounding box area is small
            if w * h < 25000:  # Threshold might need adjustment
                pyautogui.click()

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
