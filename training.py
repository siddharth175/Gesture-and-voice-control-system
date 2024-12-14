import cv2
import mediapipe as mp
import numpy as np
import time
import logging
from scipy.spatial.distance import cosine

def start_training():
    # Logger setup
    logging.basicConfig(level=logging.INFO)

    # MediaPipe Hands setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.85,
                           min_tracking_confidence=0.85)
    mp_draw = mp.solutions.drawing_utils

    # Gesture definitions with reference images
    GESTURES = [
        {"name": "next", "image_path": "gesture_images/next.jpg"},
        {"name": "previous", "image_path": "gesture_images/previous.jpg"},
        {"name": "zoom_in", "image_path": "gesture_images/zoom_in.jpg"},
        {"name": "zoom_out", "image_path": "gesture_images/zoom_out.jpg"},
        {"name": "play", "image_path": "gesture_images/play.jpg"},
        {"name": "pause", "image_path": "gesture_images/pause.jpg"},
        {"name": "volume_up", "image_path": "gesture_images/volume_up.jpg"},
        {"name": "volume_down", "image_path": "gesture_images/volume_down.jpg"},
        {"name": "scroll_up", "image_path": "gesture_images/scroll_up.jpg"},
        {"name": "scroll_down", "image_path": "gesture_images/scroll_down.jpg"}
    ]

    SIMILARITY_THRESHOLD = 0.9

    # Normalize landmarks
    def normalize_landmarks(landmarks):
        wrist = landmarks[0]
        return [[lm[0] - wrist[0], lm[1] - wrist[1], lm[2] - wrist[2]] for lm in landmarks]

    # Extract hand landmarks from an image
    def extract_landmarks_from_image(image_path):
        image = cv2.imread(image_path)
        if image is None:
            logging.warning(f"Could not load image: {image_path}")
            return None

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                return normalize_landmarks([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])

        logging.warning(f"No hand landmarks detected in reference image: {image_path}")
        return None

    # Load reference gestures
    def load_reference_gestures():
        reference_landmarks = {}
        for gesture in GESTURES:
            name = gesture["name"]
            image_path = gesture["image_path"]
            landmarks = extract_landmarks_from_image(image_path)
            if landmarks:
                reference_landmarks[name] = landmarks
            else:
                logging.warning(f"Skipping gesture: {name} (No landmarks found).")
        return reference_landmarks

    # Recognize gesture using cosine similarity
    def recognize_gesture(landmarks, reference_landmarks):
        if not landmarks or not reference_landmarks:
            return False, 0.0
        similarity = 1 - cosine(np.array(landmarks).flatten(), np.array(reference_landmarks).flatten())
        return similarity >= SIMILARITY_THRESHOLD, similarity

    # Overlay reference image on the camera feed
    def overlay_reference_image(frame, reference_image):
        if reference_image is None:
            return frame

        # Resize reference image
        ref_height, ref_width = 500, 600  # Adjusted to avoid blocking the frame
        reference_image = cv2.resize(reference_image, (ref_width, ref_height))

        # Overlay at the bottom-left corner
        frame_height, frame_width, _ = frame.shape  # Get frame dimensions
        x_offset = 10  # Margin from the left edge
        y_offset = frame_height - ref_height - 10  # Margin from the bottom edge

        # Insert the reference image into the frame
        frame[y_offset:y_offset + ref_height, x_offset:x_offset + ref_width] = reference_image
        return frame

    # Gesture practice session
    def gesture_practice_with_validation():
        reference_landmarks = load_reference_gestures()
        if not reference_landmarks:
            logging.error("No reference gestures loaded. Exiting.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Camera not accessible!")
            return

        current_index = 0
        logging.info("Starting gesture practice. Press 'n' for next gesture, 'q' to quit.")

        while True:
            success, img = cap.read()
            if not success:
                logging.error("Failed to read from camera!")
                break

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(img_rgb)

            current_gesture = GESTURES[current_index]
            gesture_name = current_gesture["name"]
            reference_image = cv2.imread(current_gesture["image_path"])

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    landmarks = normalize_landmarks([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                    recognized, similarity = recognize_gesture(landmarks, reference_landmarks[gesture_name])
                    if recognized:
                        cv2.putText(img, f"{gesture_name} (Similarity: {similarity:.2f})", (20, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Overlay reference image
            img = overlay_reference_image(img, reference_image)

            # Display the image
            cv2.imshow("Gesture Practice", img)

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord("n"):
                current_index = (current_index + 1) % len(GESTURES)
            elif key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        logging.info("Gesture practice session ended.")

    # Start gesture practice
    gesture_practice_with_validation()

if __name__ == "__main__":
    start_training()
