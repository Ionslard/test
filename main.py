import cv2
import mediapipe as mp
import mido
import time

# --- MIDI Setup ---
MIDI_PORT_NAME = 'HandTrackingMidiController'
# Create a virtual MIDI port
try:
    midi_out_port = mido.open_output(MIDI_PORT_NAME, virtual=True)
    print(f"Created virtual MIDI port: {MIDI_PORT_NAME}")
except (mido.MidiError, OSError) as e:
    print(f"Error creating virtual MIDI port: {e}")
    midi_out_port = None


# --- Note Mapping ---
def map_y_to_note(y, height):
    """Maps a y-coordinate (0 to height) to a MIDI note (0-127)."""
    # Invert y-coordinate because screen coordinates start from top-left
    inverted_y = height - y
    # Map the inverted y-coordinate to the MIDI note range
    note = int((inverted_y / height) * 127)
    return note


def main():
    """
    Captures video, tracks hands, and sends MIDI notes based on hand position.
    """
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,  # We'll start with one hand for simplicity
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    mp_drawing = mp.solutions.drawing_utils

    # Open the default webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Get frame dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    current_note = -1  # -1 means no note is currently playing

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Flip the frame horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and find hands
        results = hands.process(rgb_frame)

        # --- MIDI Logic ---
        if results.multi_hand_landmarks:
            # Get landmarks for the first hand
            hand_landmarks = results.multi_hand_landmarks[0]

            # Get the y-coordinate of the wrist (landmark 0)
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * height

            # Map the y-coordinate to a MIDI note
            note_to_play = map_y_to_note(wrist_y, height)

            # If the note has changed, send new MIDI messages
            if note_to_play != current_note:
                # Send note off for the old note
                if current_note != -1 and midi_out_port:
                    midi_out_port.send(mido.Message('note_off', note=current_note))

                # Send note on for the new note
                if midi_out_port:
                    midi_out_port.send(mido.Message('note_on', note=note_to_play, velocity=100))

                current_note = note_to_play

            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Display the current note on the screen
            cv2.putText(frame, f'Note: {current_note}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        else:
            # If no hand is detected, turn off the current note
            if current_note != -1 and midi_out_port:
                midi_out_port.send(mido.Message('note_off', note=current_note))
                current_note = -1

        # Display the resulting frame
        cv2.imshow('Hand Tracking MIDI', frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    main()
