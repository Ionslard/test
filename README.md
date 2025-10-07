# Hand Tracking MIDI Controller

This project uses your webcam to track your hand and convert its vertical position into MIDI notes, allowing you to play virtual instruments by moving your hand.

The project has been structured as a reusable Python module, and it includes a demonstration for both standard Python execution and use within a Jupyter Notebook.

## Project Structure

-   `hand_tracking_module.py`: The core module containing the `HandMusicController` class, which encapsulates all the logic for hand tracking and MIDI control.
-   `main.py`: An example script that imports the `HandMusicController` and runs the application in a standalone window.
-   `demo.ipynb`: A Jupyter Notebook that demonstrates how to use the `HandMusicController` for interactive use, displaying the webcam feed directly in the notebook.
-   `requirements.txt`: A list of Python dependencies required for the project.

## Requirements

*   Python 3.x
*   The libraries listed in `requirements.txt`:
    *   `opencv-python`
    *   `mediapipe`
    *   `mido`
    *   `python-rtmidi`
    *   `numpy`
*   For the Jupyter Notebook demo, you will also need:
    *   `jupyter`
    *   `ipython`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/hand-tracking-midi.git
    cd hand-tracking-midi
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    # If you plan to run the notebook demo, also install jupyter
    pip install jupyter ipython
    ```

## How to Use

Before you start, you need to set up a virtual MIDI device to receive the notes from this application.

### MIDI Setup

1.  **A virtual MIDI driver:** This creates a virtual MIDI "cable."
    *   **Windows:** [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) is a great, free option.
    *   **macOS:** Use the built-in **Audio MIDI Setup** utility to create a virtual port with the IAC Driver.
2.  **A synthesizer/DAW:** This is the instrument that will make sound.
    *   Examples: GarageBand (macOS), Ableton Live, FL Studio, or a simple standalone synth.

**Configuration:**
- Create a virtual MIDI port. The application will create a port named `HandTrackingMidiController` by default.
- Open your synthesizer and set its MIDI input to this virtual port.

---

### Option 1: Run as a Standalone Script

This will open a new window to display the webcam feed.

1.  **Run the script:**
    ```bash
    python main.py
    ```
2.  **Control:**
    - A window will appear showing the hand tracking.
    - Move your hand up and down to play notes.
    - Press the **'q'** key on your keyboard while the window is active to quit.

### Option 2: Run with Jupyter Notebook

This is ideal for experimentation. The webcam feed will be displayed directly inside the notebook.

1.  **Start Jupyter:**
    ```bash
    jupyter notebook
    ```
2.  **Open `demo.ipynb`:**
    - In the Jupyter interface in your browser, click on `demo.ipynb`.
3.  **Follow the instructions:**
    - The notebook contains detailed markdown cells and code cells.
    - Run the cells in order to initialize, start, and stop the hand tracking.