# Hand Tracking MIDI Controller

This project uses your webcam to track your hand movements and convert them into MIDI signals in real-time. You can use this to control virtual instruments, digital audio workstations (DAWs), or any other MIDI-compatible device.

## Description

The application captures video from your webcam and uses the MediaPipe library to detect and track your hand. The vertical position of your hand is mapped to a MIDI note, allowing you to play music by moving your hand up and down.

## Requirements

* Python 3.x
* The libraries listed in `requirements.txt`:
  * `opencv-python`
  * `mediapipe`
  * `mido`
  * `python-rtmidi`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/hand-tracking-midi.git
   cd hand-tracking-midi
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Open your MIDI software:**
   - In your DAW or virtual instrument, look for a MIDI input device named `HandTrackingMidiController`.
   - Select this device as your MIDI input.

3. **Control with your hand:**
   - A window will appear showing your webcam feed with hand tracking.
   - Move your hand up and down in front of the camera to play different MIDI notes.
   - To stop the application, press the 'q' key while the video window is active.

## How it Works

- **Video Capture:** The script uses OpenCV to capture video from your default webcam.
- **Hand Tracking:** Google's MediaPipe library is used to detect the landmarks of your hand in the video feed.
- **MIDI Mapping:** The vertical position of your wrist is mapped to a MIDI note number (0-127). As you move your hand, the note changes accordingly.
- **MIDI Output:** The `mido` library creates a virtual MIDI port that sends `note_on` and `note_off` messages to your MIDI software.
