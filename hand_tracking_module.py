import cv2
import mediapipe as mp
import mido
import time
from IPython.display import display, Image
import threading

class HandMusicController:
    """
    A class to handle hand tracking and MIDI music generation.
    """

    def __init__(self, midi_port_name='HandTrackingMidiController', max_hands=1,
                 detection_confidence=0.7, tracking_confidence=0.7, cc_control_number=1):
        """
        Initializes the HandMusicController.
        Args:
            midi_port_name (str): The name for the virtual MIDI port.
            max_hands (int): Maximum number of hands to detect.
            detection_confidence (float): Minimum confidence value for hand detection.
            tracking_confidence (float): Minimum confidence value for hand tracking.
            cc_control_number (int): The MIDI CC number to control with the x-axis.
        """
        self.midi_port_name = midi_port_name
        self.cc_control_number = cc_control_number
        self.midi_out_port = None
        self.running = False
        self.current_note = -1
        self.current_cc_value = -1

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

        # Webcam and frame dimensions
        self.cap = None
        self.width = 0
        self.height = 0

        # For Jupyter Notebook display
        self._image_widget = None


    def _setup_midi(self):
        """Creates a virtual MIDI output port."""
        try:
            self.midi_out_port = mido.open_output(self.midi_port_name, virtual=True)
            print(f"Virtual MIDI port created: {self.midi_port_name}")
        except Exception as e:
            print(f"Error creating virtual MIDI port: {e}")
            self.midi_out_port = None

    def _map_y_to_note(self, y):
        """Maps a y-coordinate to a MIDI note."""
        inverted_y = self.height - y
        return int((inverted_y / self.height) * 127)

    def _map_x_to_cc_value(self, x):
        """Maps an x-coordinate to a MIDI CC value."""
        return int((x / self.width) * 127)

    def _process_frame(self, frame):
        """
        Processes a single frame for hand tracking and MIDI control.
        """
        # Flip and convert the frame
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process for hand landmarks
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # --- Note (Y-axis) Logic ---
            wrist_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * self.height
            note_to_play = self._map_y_to_note(wrist_y)

            if note_to_play != self.current_note:
                if self.current_note != -1 and self.midi_out_port:
                    self.midi_out_port.send(mido.Message('note_off', note=self.current_note))

                if self.midi_out_port:
                    self.midi_out_port.send(mido.Message('note_on', note=note_to_play, velocity=100))

                self.current_note = note_to_play

            # --- CC (X-axis) Logic ---
            wrist_x = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * self.width
            cc_value_to_send = self._map_x_to_cc_value(wrist_x)

            if cc_value_to_send != self.current_cc_value and self.midi_out_port:
                self.midi_out_port.send(mido.Message('control_change', control=self.cc_control_number, value=cc_value_to_send))
                self.current_cc_value = cc_value_to_send

            # Drawing landmarks and info on the frame
            self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, f'Note: {self.current_note}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'CC {self.cc_control_number}: {self.current_cc_value}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            # If no hand is detected, turn off the current note
            if self.current_note != -1 and self.midi_out_port:
                self.midi_out_port.send(mido.Message('note_off', note=self.current_note))
                self.current_note = -1

        return frame

    def start_notebook_display(self):
        """
        Starts the hand tracking loop and displays the output in a Jupyter Notebook.
        """
        if self.running:
            print("Controller is already running.")
            return

        self._setup_midi()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self._image_widget = display(Image(b''), display_id=True)

        self.running = True
        self.thread = threading.Thread(target=self._notebook_update_loop)
        self.thread.start()
        print("Hand tracking started for Jupyter Notebook.")

    def _notebook_update_loop(self):
        """The loop that continuously updates the image in the notebook."""
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            processed_frame = self._process_frame(frame)

            # Convert frame to JPEG format
            _, jpg_frame = cv2.imencode('.jpeg', processed_frame)

            # Update the image widget
            self._image_widget.update(Image(data=jpg_frame.tobytes()))

        self.stop() # Clean up when loop ends

    def start_window_display(self):
        """
        Starts the hand tracking loop and displays the output in a separate window.
        """
        if self.running:
            print("Controller is already running.")
            return

        self._setup_midi()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.running = True
        print("Hand tracking started. Press 'q' in the window to quit.")

        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            processed_frame = self._process_frame(frame)
            cv2.imshow('Hand Tracking MIDI', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.stop()

    def stop(self):
        """Stops the hand tracking and releases resources."""
        if not self.running:
            return

        self.running = False
        # Wait for the thread to finish if it exists
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()

        if self.current_note != -1 and self.midi_out_port:
            self.midi_out_port.send(mido.Message('note_off', note=self.current_note))

        if self.cap:
            self.cap.release()

        cv2.destroyAllWindows()
        self.hands.close()

        if self.midi_out_port:
            self.midi_out_port.close()

        print("Hand tracking stopped.")