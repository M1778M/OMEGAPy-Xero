import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout,
    QLineEdit, QComboBox, QPushButton, QWidget
)
from PyQt6.QtCore import Qt

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Login Page")
        self.setFixedSize(300, 200)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        # Title
        title = QLabel("Login to API")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # API selection
        self.api_selector = QComboBox()
        self.api_selector.addItems(["Select API", "ChatGPT", "Groq", "Together"])
        self.api_selector.setStyleSheet("padding: 5px;")
        layout.addWidget(self.api_selector)

        # API key input
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter API Key")
        self.api_key_input.setStyleSheet("padding: 5px;")
        layout.addWidget(self.api_key_input)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """)
        self.submit_button.clicked.connect(self.handle_submit)
        layout.addWidget(self.submit_button)

    def handle_submit(self):
        # Gather user input
        selected_api = self.api_selector.currentText()
        api_key = self.api_key_input.text().strip()

        # Validation
        if selected_api == "Select API" or not api_key:
            error_message = "Please select an API and enter a valid API key."
            self.show_error_message(error_message)
            return

        # Save config
        config_data = {
            "api": selected_api,
            "api_key": api_key
        }
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file, indent=4)

        # Close the application
        self.close()

    def show_error_message(self, message):
        error_dialog = QLabel(message)
        error_dialog.setStyleSheet("color: red; font-size: 12px;")
        self.central_widget.layout().addWidget(error_dialog)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())
