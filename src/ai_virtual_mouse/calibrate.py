# src/ai_virtual_mouse/calibrate.py

from pathlib import Path

import cv2
import yaml

from ai_virtual_mouse.hand_tracker import HandTracker

CONFIG_PATH = Path("config.yaml")


def calibrate_hand_range():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    print("\n[🖐️] Calibration started.")
    print("Move your hand to all corners of the region you'd like to use.")
    print("Press 'q' when done.\n")

    x_min, y_min = float("inf"), float("inf")
    x_max, y_max = float("-inf"), float("-inf")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        tracker.find_hands(frame, draw=True)
        landmarks = tracker.get_landmark_positions(frame)

        if landmarks:
            for _, x, y in landmarks:
                h, w, _ = frame.shape
                x_norm = x / w
                y_norm = y / h

                x_min = min(x_min, x_norm)
                y_min = min(y_min, y_norm)
                x_max = max(x_max, x_norm)
                y_max = max(y_max, y_norm)

        # Visual guide
        cv2.putText(
            frame,
            "Press 'q' to finish calibration",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
        cv2.imshow("Calibration", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    roi = {
        "enabled": True,
        "x_min": round(x_min, 3),
        "x_max": round(x_max, 3),
        "y_min": round(y_min, 3),
        "y_max": round(y_max, 3),
    }

    print("\n[✅] Calibration complete.")
    print("ROI:", roi)

    _update_config_roi(roi)
    print(f"[💾] Updated {CONFIG_PATH} with new region_of_interest.")


def _update_config_roi(new_roi: dict):
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config.yaml not found.")

    with CONFIG_PATH.open("r") as f:
        config = yaml.safe_load(f)

    config["region_of_interest"] = new_roi

    with CONFIG_PATH.open("w") as f:
        yaml.dump(config, f, sort_keys=False)


if __name__ == "__main__":
    calibrate_hand_range()
