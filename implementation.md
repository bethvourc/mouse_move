# Implementation Plan

## 1 ‒ Project Skeleton & Tooling

- [x] **Step 1: Bootstrap Poetry project**

  - **Task**: Create a Python‑package layout (`pyproject.toml`, `src/ai_virtual_mouse/__init__.py`) with Poetry.
  - **Description**: Provides isolated dependency management and prepares the codebase for packaging.
  - **Files**:
    - `pyproject.toml`: new
    - `src/ai_virtual_mouse/__init__.py`: new
  - **Step Dependencies**: none
  - **User Instructions**: Run `poetry init` and accept defaults.

- [x] **Step 2: Add static‑analysis tooling**
  - **Task**: Configure _black_, _ruff_, and _pre‑commit_ hooks.
  - **Description**: Enforces code style automatically on every commit.
  - **Files**:
    - `.pre-commit-config.yaml`: new
    - `pyproject.toml`: update
  - **Step Dependencies**: 1
  - **User Instructions**: `poetry add --group dev black ruff pre-commit && pre-commit install`.

## 2 ‒ Core Input Pipeline

- [x] **Step 3: Refactor video capture to a `Camera` class**

  - **Task**: Wrap `cv2.VideoCapture` plus resolution getters into `camera.py`.
  - **Description**: Encapsulates camera handling for easier testing and future multi‑camera support.
  - **Files**:
    - `src/ai_virtual_mouse/camera.py`: new
    - `AIVirtualMouseProject.py`: migrate capture code
  - **Step Dependencies**: 1
  - **User Instructions**: None (AI will move code).

- [x] **Step 4: Replace color segmentation with MediaPipe Hands**
  - **Task**: Create `hand_detector.py` leveraging `mediapipe.solutions.hands`.
  - **Description**: Increases robustness across lighting and skin tones compared with the current HSV mask approach.
  - **Files**:
    - `src/ai_virtual_mouse/hand_detector.py`: new
  - **Step Dependencies**: 3
  - **User Instructions**: `poetry add mediapipe`.

## 3 ‒ Gesture Recognition

- [x] **Step 5: Implement landmark‑based gesture utilities**

  - **Task**: Add helpers to obtain fingertip positions and distances.
  - **Description**: Forms the basis for click, right‑click, drag & scroll gestures.
  - **Files**:
    - `src/ai_virtual_mouse/gestures.py`: new
  - **Step Dependencies**: 4

- [x] **Step 6: Create `GestureClassifier` for common actions**
  - **Task**: Classify landmarks into _left click_, _right click_, _scroll_ based on configurable rules.
  - **Description**: Extends functionality beyond the current single “small bbox = click” heuristic.
  - **Files**:
    - `src/ai_virtual_mouse/gesture_classifier.py`: new
  - **Step Dependencies**: 5

## 4 ‒ Cursor Control & Smoothing

- [x] **Step 7: Introduce `MouseController` abstraction**

  - **Task**: Wrap PyAutoGUI calls (`moveTo`, `click`, `scroll`).
  - **Description**: Centralizes OS‑interaction logic and eases mocking in tests.
  - **Files**:
    - `src/ai_virtual_mouse/mouse_controller.py`: new
  - **Step Dependencies**: 3

- [x] **Step 8: Add exponential moving‑average smoothing**
  - **Task**: Implement optional `Smoother` to dampen jitter.
  - **Description**: Produces steadier cursor movement.
  - **Files**:
    - `src/ai_virtual_mouse/smoothing.py`: new
  - **Step Dependencies**: 7

## 5 ‒ Calibration & Configuration

- [x] **Step 9: YAML‑based runtime config**

  - **Task**: Load sensitivities, gesture thresholds, and region‑of‑interest from `config.yaml`.
  - **Description**: Lets users tune performance without code edits.
  - **Files**:
    - `config.yaml`: new
    - `src/ai_virtual_mouse/config.py`: new
  - **Step Dependencies**: 6, 8

- [x] **Step 10: Interactive calibration wizard**
  - **Task**: CLI flow that guides users through hand‑range mapping and saves values back to `config.yaml`.
  - **Files**:
    - `src/ai_virtual_mouse/calibrate.py`: new
  - **Step Dependencies**: 9

## 6 ‒ User Interface & Feedback

- [x] **Step 11: On‑screen overlay for visual cues**
  - **Task**: Draw landmarks and action labels in OpenCV window with minimal latency.
  - **Description**: Improves UX and debugging.
  - **Files**:
    - `src/ai_virtual_mouse/overlay.py`: new
  - **Step Dependencies**: 6

## 7 ‒ Performance & Threading

- [ ] **Step 12: Move inference to background thread**
  - **Task**: Use `concurrent.futures.ThreadPoolExecutor` to decouple capture, inference, and UI.
  - **Description**: Reduces end‑to‑end lag on lower‑spec machines.
  - **Files**:
    - `src/ai_virtual_mouse/threading.py`: new
  - **Step Dependencies**: 4, 7

## 8 ‒ Testing & Continuous Integration

- [ ] **Step 13: Unit tests for utility modules**

  - **Task**: Add pytest cases for `smoothing.py`, `gestures.py`, and `config.py`.
  - **Files** (≤ 10):
    - `tests/test_smoothing.py`, etc.
  - **Step Dependencies**: 5, 8, 9
  - **User Instructions**: `poetry add --group dev pytest && pytest -q`.

- [ ] **Step 14: Integration test with prerecorded frames**

  - **Task**: Validate end‑to‑end gesture→mouse event sequence via PyAutoGUI mock.
  - **Files**:
    - `tests/test_e2e.py`: new
    - `tests/fixtures/frames/*.jpg`: new
  - **Step Dependencies**: 6, 7, 8

- [ ] **Step 15: GitHub Actions workflow**
  - **Task**: Lint, unit, integration tests on push.
  - **Files**:
    - `.github/workflows/ci.yaml`: new
  - **Step Dependencies**: 13, 14

## 9 ‒ Packaging & Distribution

- [ ] **Step 16: CLI entry‑point**

  - **Task**: Add `python -m ai_virtual_mouse` bootstrapping using `if __name__ == "__main__"`.
  - **Files**:
    - `src/ai_virtual_mouse/__main__.py`: new
  - **Step Dependencies**: 10, 11, 12

- [ ] **Step 17: Build Dockerfile & publish to PyPI**
  - **Task**: Provide containerized run option; configure Poetry publish workflow.
  - **Files**:
    - `Dockerfile`: new
    - `Makefile`: new
  - **Step Dependencies**: 16

## 10 ‒ Documentation & Demo Assets

- [ ] **Step 18: Sphinx docs site with MkDocs theme**

  - **Task**: Autogenerate API docs from docstrings; host on GitHub Pages.
  - **Files**:
    - `docs/`: new
  - **Step Dependencies**: 16

- [ ] **Step 19: Update README with GIF demo & feature matrix**
  - **Task**: Replace existing README section with new capabilities list and animated preview.
  - **Files**:
    - `README.md`: update
    - `assets/demo.gif`: new
  - **Step Dependencies**: 16, 18
