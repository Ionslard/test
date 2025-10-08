# Hand Tracking MIDI Controller

This project uses your webcam to track your hand and convert its position into MIDI signals, allowing you to play and modulate virtual instruments in real-time.

The project is structured as a reusable Python module and includes demonstrations for both standard Python execution and use within a Jupyter Notebook.

## Features

-   **Note Control (Y-axis):** The vertical position of your hand is mapped to a MIDI note (0-127). Move your hand up and down to play different notes.
-   **Modulation Control (X-axis):** The horizontal position of your hand is mapped to a MIDI Control Change (CC) value. By default, it controls **CC #1 (Modulation)**, but it can be configured for other parameters.
-   **Jupyter Notebook Integration:** Display the webcam feed and control the instrument directly within a Jupyter Notebook.
-   **Configurable:** Easily change the MIDI port name and the CC control number.

## Project Structure

-   `hand_tracking_module.py`: The core module containing the `HandMusicController` class.
-   `main.py`: An example script to run the application in a standalone window.
-   `demo.ipynb`: A Jupyter Notebook that demonstrates interactive use.
-   `requirements.txt`: A list of Python dependencies.

## Requirements

*   Python 3.x
*   The libraries listed in `requirements.txt`.
*   For the Jupyter Notebook demo: `jupyter` and `ipython`.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/hand-tracking-midi.git
    cd hand-tracking-midi
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

### 1. MIDI Setup

Before you start, you need a virtual MIDI device to receive the notes.

-   **Virtual MIDI Driver:**
    -   **Windows:** [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
    -   **macOS:** Use the built-in **Audio MIDI Setup** utility (IAC Driver).
-   **Synthesizer/DAW:**
    -   Examples: GarageBand, Ableton Live, FL Studio.

**Configuration:** Create a virtual MIDI port. Then, open your synthesizer and set its MIDI input to this virtual port. The app will create a port named `HandTrackingMidiController` by default.

### 2. Running the Application

#### Option A: Standalone Script

This opens a new window for the webcam feed.

1.  **Run the script:**
    ```bash
    python main.py
    ```
2.  **Control:**
    -   Move your hand **up and down** to play notes.
    -   Move your hand **left and right** to change the modulation value (CC #1).
    -   Press **'q'** to quit.

#### Option B: Jupyter Notebook

This is ideal for experimentation, showing the feed directly in the notebook.

1.  **Start Jupyter:**
    ```bash
    jupyter notebook
    ```
2.  **Open `demo.ipynb`** and run the cells in order. The notebook provides detailed instructions.

## Customization

You can customize the `HandMusicController` when you create an instance. For example, to control **Volume (CC #7)** instead of Modulation:

```python
from hand_tracking_module import HandMusicController

# Control Volume (CC #7) with the X-axis
controller = HandMusicController(cc_control_number=7)

# Start the controller
controller.start_window_display() # or start_notebook_display()
```