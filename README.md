# AI Virtual Mouse Project

The AI Virtual Mouse Project is a Python application that enables the control of the mouse cursor using hand movements captured through a webcam. This project uses computer vision techniques to detect hand movements and translate them into mouse actions on the screen.

## Features

- Hand detection using color segmentation
- Movement of the mouse cursor corresponding to the detected hand's position
- Simple click action based on the size of the detected hand area

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- PyAutoGUI

## Installation

To run the AI Virtual Mouse Project, you need to have Python installed on your system. If you haven't installed Python yet, download and install it from the [official Python website](https://www.python.org/downloads/).

After installing Python, you can install the required libraries using pip. Open your terminal or command prompt and run the following commands:

```bash
pip install opencv-python
pip install numpy
pip install pyautogui
```

## Usage

1. Ensure your webcam is connected and properly set up.
2. Clone the repository or download the `AIVirtualMouseProject.py` file to your local machine.
3. Open a terminal or command prompt and navigate to the directory containing `AIVirtualMouseProject.py`.
4. Run the script by executing the command:
   ```bash
   python AIVirtualMouseProject.py
   ```
5. Once the application starts, it will use your webcam to detect your hand's movement. Move your hand to control the mouse cursor.
6. To perform a click action, make your hand's detected area small (e.g., by making a fist).
7. To exit the application, press the 'q' key while the webcam window is active.

## Configuration

The hand detection sensitivity can be adjusted by changing the `hsv_lower` and `hsv_upper` values in the `ColorHandDetector` class initialization within the `main()` function.

## Limitations

- The application currently does not support right-click or scroll actions.
- Performance may vary based on lighting conditions and webcam quality.

## Contributions

Contributions to the AI Virtual Mouse Project are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

---