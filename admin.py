import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QWidget, QMessageBox)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import subprocess
import threading

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# Function to trigger `take_image.py`
def trigger_take_image():
    subprocess.run(["python", "take_image.py"])

# Function to trigger `capture_gestures`
def trigger_capture_gestures():
    from your_module import YourClass  # Replace with your actual module and class names
    obj = YourClass()
    obj.capture_gestures()

# Main Window class
class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")

        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QPushButton#exitButton {
                background-color: #D32F2F;
                color: white;
            }
            QPushButton#exitButton:hover {
                background-color: #B71C1C;
            }
            QPushButton#exitButton:pressed {
                background-color: #7F0000;
            }
            QLineEdit {
                background-color: #2C2C2C;
                color: white;
                border: 1px solid #3C3C3C;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Set window size
        self.resize(300, 300)

        # Login screen layout
        self.login_widget = QWidget()
        self.login_layout = QVBoxLayout()

        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.handle_login)

        self.login_layout.addWidget(self.label_username)
        self.login_layout.addWidget(self.input_username)
        self.login_layout.addWidget(self.label_password)
        self.login_layout.addWidget(self.input_password)
        self.login_layout.addWidget(self.button_login)

        self.login_widget.setLayout(self.login_layout)
        self.setCentralWidget(self.login_widget)

        # Admin panel setup
        self.admin_widget = QWidget()
        self.admin_layout = QVBoxLayout()

        self.button_take_image = QPushButton("Take Image")
        self.button_take_image.clicked.connect(self.start_take_image)

        self.button_capture_gestures = QPushButton("Capture Gestures")
        self.button_capture_gestures.clicked.connect(self.start_capture_gestures)

        self.button_exit = QPushButton("Exit")
        self.button_exit.setObjectName("exitButton")
        self.button_exit.clicked.connect(self.close_application)

        self.admin_layout.addWidget(self.button_take_image)
        self.admin_layout.addWidget(self.button_capture_gestures)
        self.admin_layout.addWidget(self.button_exit)

        self.admin_widget.setLayout(self.admin_layout)

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.setCentralWidget(self.admin_widget)
            self.setWindowTitle("Admin Panel")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials. Please try again.")

    def start_take_image(self):
        threading.Thread(target=trigger_take_image).start()
        QMessageBox.information(self, "Success", "take_image.py script triggered successfully!")

    def start_capture_gestures(self):
        threading.Thread(target=trigger_capture_gestures).start()
        QMessageBox.information(self, "Success", "capture_gestures function triggered successfully!")

    def close_application(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = AdminApp()
    main_window.show()

    sys.exit(app.exec_())
