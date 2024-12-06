import cv2
import mediapipe as mp
import numpy as np
import time  # For adding delay

# Define a list of 3 colors (Red, Green, Blue)
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # Red, Green, Blue
current_color_index = 0  # Initially set to the first color (Red)

# Time tracking for delay
last_color_change_time = 0
color_change_delay = 1  # Delay in seconds

def start_drawing():
    global current_color_index, last_color_change_time  # Use the global color index and last time

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.7,
                           min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    # Canvas settings
    canvas = None
    brush_thickness = 5
    eraser_thickness = 50

    # Gesture states
    is_drawing = False
    prev_x, prev_y = 0, 0

    # OpenCV Window
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)  # Flip the frame for a mirror effect
        h, w, _ = frame.shape
        if canvas is None:
            canvas = np.zeros((h, w, 3), dtype=np.uint8)

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract landmark positions
                landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
                index_finger = landmarks[8]
                middle_finger = landmarks[12]
                ring_finger = landmarks[16]
                pinky_finger = landmarks[20]

                # Gesture Detection
                num_fingers_up = sum(
                    1 for lm in [index_finger, middle_finger, ring_finger, pinky_finger] if lm[1] < landmarks[5][1])

                # Index Finger Only - Drawing
                if num_fingers_up == 1:
                    cv2.circle(frame, index_finger, 10, colors[current_color_index], cv2.FILLED)
                    if is_drawing:
                        cv2.line(canvas, (prev_x, prev_y), index_finger, colors[current_color_index], brush_thickness)
                    is_drawing = True
                    prev_x, prev_y = index_finger

                # Two Fingers - Move (you can add functionality here if needed)
                elif num_fingers_up == 2:
                    is_drawing = False
                    cv2.putText(frame, "Move Mode", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # All Fingers - Erase (Clear Canvas)
                elif num_fingers_up == 5:
                    is_drawing = False
                    cv2.putText(frame, "Eraser Mode", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.rectangle(canvas, (0, 0), (w, h), (0, 0, 0), cv2.FILLED)

                # Three Fingers - Change Color (with delay)
                elif num_fingers_up == 3:
                    current_time = time.time()
                    # Only change the color if the delay has passed
                    if current_time - last_color_change_time > color_change_delay:
                        current_color_index = (current_color_index + 1) % len(colors)  # Cycle through the 3 colors
                        last_color_change_time = current_time  # Update the last time color was changed
                        cv2.putText(frame, f"Color: {colors[current_color_index]}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # Fist Gesture - Clear the Canvas
                elif all(lm[1] > landmarks[5][1] for lm in [index_finger, middle_finger, ring_finger, pinky_finger]):
                    # Fist detected (all fingers down)
                    cv2.putText(frame, "Clear Screen", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    canvas = np.zeros((h, w, 3), dtype=np.uint8)  # Clear the canvas

        # Merge the canvas and frame
        frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

        # Display the result
        cv2.imshow("Virtual Drawing", frame)

        # Key controls
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):  # Quit
            break
        elif key & 0xFF == ord('c'):  # Clear canvas (manual option)
            canvas = np.zeros((h, w, 3), dtype=np.uint8)

    cap.release()
    cv2.destroyAllWindows()
