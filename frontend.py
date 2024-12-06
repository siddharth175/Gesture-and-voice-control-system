import sys
import main


from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
import draw  # Import your backend file

class ControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesture and Voice Control")
        self.setGeometry(100, 100, 400, 300)

        # Apply dark theme with background
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
                background-image: url('background.jpg');  /* Replace with your background image path */
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
        """)

        # Create UI elements
        self.init_ui()

    def init_ui(self):
        # Central Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title Label
        self.title_label = QLabel("Gesture and Voice Control System", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #FDFEFE;
            margin: 10px;
        """)
        layout.addWidget(self.title_label)

        # Start Control Button
        self.start_btn = self.create_button("Start Control", self.start_control)
        layout.addWidget(self.start_btn)

        # Start Drawing Button
        self.drawing_btn = self.create_button("Start Drawing", self.start_drawing)
        layout.addWidget(self.drawing_btn)

        # Capture Gestures Button
        self.capture_btn = self.create_button("Capture Gestures", self.capture_gestures)
        layout.addWidget(self.capture_btn)

        # Exit Button
        self.exit_btn = self.create_button("Exit", self.close_application, is_exit=True)
        layout.addWidget(self.exit_btn)

    def create_button(self, text, callback, is_exit=False):
        """Helper function to create styled buttons with hover effects."""
        button = QPushButton(text, self)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#E74C3C' if is_exit else '#3498DB'};
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                margin: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: {'#C0392B' if is_exit else '#2980B9'};
            }}
        """)
        button.clicked.connect(callback)
        return button

    def start_control(self):
        """Start gesture and voice control."""
        try:
            main.start_control()  # Call backend control function
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def start_drawing(self):
        """Start the drawing application."""
        try:
            draw.start_drawing()  # Call the start_drawing function from main.py
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")


    def capture_gestures(self):
        """Start gesture capture setup."""
        try:
            main.capture_gestures()  # Call backend gesture capture function
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def close_application(self):
        """Exit the application."""
        self.close()

# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ControlWindow()
    window.show()
    sys.exit(app.exec_())
