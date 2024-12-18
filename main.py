import os
import warnings
import platform
import cv2
import mediapipe as mp
import json
import numpy as np
import pyautogui
import subprocess
import time
import speech_recognition as sr
import logging
from queue import Queue
from threading import Thread
from scipy.spatial.distance import cosine
from gtts import gTTS
import playsound

# Suppress TensorFlow Lite and other warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

# Logger setup
logging.basicConfig(level=logging.INFO)
logging.info("Starting gesture and voice control...")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, 
                       max_num_hands=1, 
                       min_detection_confidence=0.85, 
                       min_tracking_confidence=0.85)
mp_draw = mp.solutions.drawing_utils

# File path for storing gestures
GESTURE_FILE = 'gestures.json'
SIMILARITY_THRESHOLD = 0.9  # Configurable threshold for gesture recognition
ACTION_DELAY = 2  # Delay in seconds between consecutive actions
action_queue = Queue()  # Thread-safe queue for actions

# Normalization Function
def normalize_landmarks(landmarks):
    wrist = landmarks[0]
    return [[lm[0] - wrist[0], lm[1] - wrist[1], lm[2] - wrist[2]] for lm in landmarks]

# Gesture File Management
def save_gestures(gesture_data):
    with open(GESTURE_FILE, 'w') as f:
        json.dump(gesture_data, f, indent=4)
    logging.info("All gestures saved successfully!")

def load_gestures():
    try:
        with open(GESTURE_FILE, 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Gesture file format invalid.")
            return data
    except FileNotFoundError:
        logging.warning("No gestures found! Please define gestures first.")
        return {}
    except ValueError as e:
        logging.error(f"Error loading gestures: {e}")
        return {}

# Gesture Capture Function
def capture_gestures():
    gestures_to_capture = ["next", "previous", "zoom in", "zoom out", "play", "pause", "mute", "volume up", "volume down", "scroll up", "scroll down"]
    samples_per_gesture = 5
    gesture_data = {}

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Camera not accessible!")
        return

    logging.info("Gesture setup phase started. Press 's' to save each sample or 'q' to quit.")

    for gesture_name in gestures_to_capture:
        logging.info(f"Perform the gesture for '{gesture_name}'. Press 's' to save.")
        gesture_data[gesture_name] = []

        while len(gesture_data[gesture_name]) < samples_per_gesture:
            success, img = cap.read()
            if not success:
                logging.error("Camera not accessible!")
                break

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(img_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmarks = normalize_landmarks([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])

                    cv2.putText(img, f"Perform: {gesture_name} ({len(gesture_data[gesture_name])+1}/5)", 
                                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        gesture_data[gesture_name].append(landmarks)
                        logging.info(f"Sample {len(gesture_data[gesture_name])} for '{gesture_name}' saved.")
                        time.sleep(0.5)
                        break

            cv2.imshow("Gesture Capture", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info("Gesture setup interrupted.")
                cap.release()
                cv2.destroyAllWindows()
                return

    cap.release()
    cv2.destroyAllWindows()
    save_gestures(gesture_data)

# Gesture Recognition
def recognize_gesture(landmarks, saved_gestures):
    best_match = None
    highest_similarity = 0
    for name, samples in saved_gestures.items():
        for sample in samples:
            similarity = 1 - cosine(np.array(landmarks).flatten(), np.array(sample).flatten())
            if similarity > highest_similarity and similarity > SIMILARITY_THRESHOLD:
                highest_similarity = similarity
                best_match = name
    return best_match, highest_similarity

# Perform Actions
def perform_action(action):
    # Define the modifier key for macOS (Command key)
    modifier = 'command'

    if action == 'next':
        pyautogui.press('right')
    elif action == 'previous':
        pyautogui.press('left')
    elif action == 'zoom in':
        pyautogui.hotkey(modifier, '+')
    elif action == 'zoom out':
        pyautogui.hotkey(modifier, '-')
    elif action in ['play', 'pause']:
        pyautogui.press('space')
    elif action == 'mute':
        subprocess.run(['osascript', '-e', 'set volume output muted true'])
    elif action == 'volume up':
        subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 20)'])
    elif action == 'volume down':
        subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 20)'])
    elif action == 'scroll up':
        pyautogui.scroll(10)  # Scroll up
    elif action == 'scroll down':
        pyautogui.scroll(-10)  # Scroll down
    else:
        logging.warning(f"Action '{action}' is not defined!")

# Enhanced Voice Command Recognition with Wake-up Word
def recognize_voice_command(wakeup_word="apple"):
    recognizer = sr.Recognizer()
    expected_commands = ["next", "previous", "zoom in", "zoom out", "play", "pause", "mute", "volume up", "volume down", "scroll up", "scroll down"]

    with sr.Microphone() as source:
        while True:
            try:
                logging.info(f"Listening for wake-up command '{wakeup_word}'...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = recognizer.recognize_google(audio).lower()

                if wakeup_word in command:
                    logging.info(f"Wake-up word '{wakeup_word}' detected.")
                    # Use gTTS to speak confirmation
                    tts = gTTS(text="Say command", lang='en')
                    tts.save("say_command.mp3")
                    playsound.playsound("say_command.mp3")
                    os.remove("say_command.mp3")

                    # Now listen for the actual command
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio).lower()

                    if command in expected_commands:
                        logging.info(f"Command '{command}' accepted.")
                        tts = gTTS(text=f"Command {command} accepted", lang='en')
                        tts.save("command_accepted.mp3")
                        playsound.playsound("command_accepted.mp3")
                        os.remove("command_accepted.mp3")
                        return command
                    else:
                        logging.warning(f"Command '{command}' not recognized.")
                        tts = gTTS(text="Command not recognized, please try again", lang='en')
                        tts.save("command_not_recognized.mp3")
                        playsound.playsound("command_not_recognized.mp3")
                        os.remove("command_not_recognized.mp3")

                else:
                    logging.warning(f"Wake-up word '{wakeup_word}' not detected.")
                    continue

            except sr.UnknownValueError:
                logging.warning("Speech not understood. Retrying...")
                continue
            except sr.RequestError as e:
                logging.error(f"Request failed; {e}")
                break
            except Exception as e:
                logging.error(f"Error during voice recognition: {e}")
                break

# Combined Gesture and Voice Control
def start_control():
    saved_gestures = load_gestures()
    if not saved_gestures:
        logging.warning("No gestures available. Define gestures first!")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Camera not accessible!")
        return

    last_action_time = 0
    detected_action = ""
    similarity_score = 0

    def voice_thread():
        while True:
            command = recognize_voice_command()  # Wait for wake-up command
            if command:
                action_queue.put(command)

    Thread(target=voice_thread, daemon=True).start()

    while True:
        success, img = cap.read()
        if not success:
            logging.error("Camera not accessible!")
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                landmarks = normalize_landmarks([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                detected_gesture, similarity = recognize_gesture(landmarks, saved_gestures)

                if detected_gesture and similarity >= SIMILARITY_THRESHOLD:
                    detected_action = detected_gesture
                    similarity_score = similarity
                else:
                    detected_action = None
                    similarity_score = 0

                if detected_action and time.time() - last_action_time > ACTION_DELAY:
                    action_queue.put(detected_action)
                    last_action_time = time.time()

        if not action_queue.empty():
            action = action_queue.get()
            if action:
                logging.info(f"Performing action: {action}")
                perform_action(action)

        # Display gestures and landmarks
        if detected_action:
            cv2.putText(img, f"Detected Gesture: {detected_action} ({round(similarity_score*100, 2)}%)", 
                        (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Gesture and Voice Control", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_control()
