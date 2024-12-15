# ✨ Gesture & Voice Control System ✨  

Welcome to the **Gesture & Voice Control System**, an innovative project that lets you control presentations, videos, and even digital art using hand gestures and voice commands.  

This system offers a seamless, interactive experience, eliminating the need for physical interaction with devices. It interprets gestures, executes predefined actions, and responds to voice commands for enhanced usability.  

---

## 🌟 Key Features  

### ✋ Gesture Control  

#### Slide Navigation  
- **Next Slide**: Swipe or perform a forward gesture to move to the next slide.  
- **Previous Slide**: Swipe backward or use a backward gesture to return to the previous slide.  

#### Zoom Control  
- **Zoom In**: Spread your fingers apart to zoom into the current slide.  
- **Zoom Out**: Bring your fingers together to zoom out.  

#### Media Playback Control  
- **Play/Pause**: Start or stop video playback using a gesture.  
- **Skip Forward/Backward**: Move the video forward or backward by 5 seconds using gestures.  
- **Volume Control**:  
  - **Volume Up**: Swipe upwards to increase the volume.  
  - **Volume Down**: Swipe downwards to decrease the volume.  

#### Scrolling Control (New!)  
- **Scroll Up**: Use a "scroll up" gesture to move content upwards.  
- **Scroll Down**: Use a "scroll down" gesture to move content downwards.  

---

### 🎤 Voice Commands  

#### Slide Navigation  
- **"Next"**: Move to the next slide.  
- **"Previous"**: Return to the previous slide.  

#### Zoom Control  
- **"Zoom In"**: Zoom into the current slide.  
- **"Zoom Out"**: Zoom out of the slide.  

#### Media Playback  
- **"Play"**: Start video playback.  
- **"Pause"**: Pause the video.  
- **"Volume Up"**: Increase the volume.  
- **"Volume Down"**: Decrease the volume.  

#### Scrolling Control (New!)  
- **"Scroll Up"**: Move the content upwards.  
- **"Scroll Down"**: Move the content downwards.  

---

### 🎨 Real-Time Drawing  

- **Freehand Drawing**: Draw on a digital canvas using hand gestures.  
- **Erase Mode**: Switch to erasing mode with a gesture.  
- **Move Mode**: Move the canvas or your drawing with specific gestures.  

---

### 🔧 Training Mode (New!)  

- Introduces new users to the system by demonstrating gesture recognition and voice command functionalities.  
- Provides interactive tutorials for mastering gesture and voice controls.  
- Enables users to practice and refine their gestures and commands in a guided environment.  

---

### 🔐 Admin Pages (New!)  

- **Admin Login**: Access admin settings with the following credentials:  
  - **Username**: `admin`  
  - **Password**: `password`  
- **Features**:  
  - View system logs and user activities.  
  - Manage gestures and voice commands.  
  - Update application settings and preferences.  

---

## 💻 Tech Stack  

- **Frontend**:  
  - [PyQt5](https://riverbankcomputing.com/software/pyqt/intro): For creating an interactive GUI.  

- **Gesture Recognition**:  
  - [MediaPipe](https://mediapipe.dev/): Google's open-source library for hand tracking and gesture recognition.  

- **Voice Recognition**:  
  - [SpeechRecognition](https://pypi.org/project/SpeechRecognition/): Converts speech to text to detect voice commands.  

- **Automation**:  
  - [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/): Simulates keyboard and mouse actions for automation.  

---

## 🚀 Getting Started  

### Clone the Repository  
```bash  
git clone https://github.com/your-username/gesture-voice-control.git  
cd gesture-voice-control  
```  

### Install Dependencies  
Ensure Python 3.x is installed. Then, install the required dependencies:  
```bash  
pip install -r requirements.txt  
```  

### Run the Application  
Start the application with:  
```bash  
python frontend.py  
```  

---

## 🔧 Usage  

### Gesture Control  

#### Slide Navigation  
- **Next Slide**: Swipe or move your hand forward.  
- **Previous Slide**: Swipe backward or move your hand backward.  

#### Zoom Control  
- **Zoom In**: Spread fingers apart.  
- **Zoom Out**: Pinch fingers together.  

#### Media Playback  
- **Play/Pause**: Start or stop playback using a gesture.  
- **Skip Forward/Backward**: Move the video 5 seconds forward or backward using gestures.  

#### Volume Control  
- **Volume Up**: Swipe upwards.  
- **Volume Down**: Swipe downwards.  

#### Scrolling Control  
- **Scroll Up**: Perform a "scroll up" gesture.  
- **Scroll Down**: Perform a "scroll down" gesture.  

### Voice Commands  

- **"Next"**, **"Previous"**: Navigate slides.  
- **"Zoom In"**, **"Zoom Out"**: Adjust zoom levels.  
- **"Play"**, **"Pause"**, **"Volume Up"**, **"Volume Down"**: Control media playback.  
- **"Scroll Up"**, **"Scroll Down"**: Control scrolling.  

### Drawing Modes  

- **Drawing Mode**: Draw freely on the screen.  
- **Erase Mode**: Erase parts of your drawing using gestures.  
- **Move Mode**: Move the canvas or drawing with gestures.  

---

## 🗣️ Custom Voice Commands  

1. Modify the `recognize_voice_command()` function.  
2. Map new commands to specific actions (e.g., custom slide transitions).  
3. Save and use your custom commands in the system.  

---

## 🎨 Customizing Gestures  

1. **Capture Gesture**: Use the GUI to record a new gesture.  
2. **Assign Action**: Map the gesture to an action (e.g., "Zoom In").  
3. **Save Gesture**: Save for future use.  

---

## 🎥 Demo  

Check out the https://youtu.be/eoM_FcPw1d4 to see the system in action!  

---

**Enjoy a smarter way to interact with your digital world!**

