from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("OMEGAPy-Xero Chatmode")
        self.setFixedSize(400, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2a2a2a;
            }
        """)
        self._main_window = None
        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Chat display
        self.chat_display = QTextBrowser()
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Arial', sans-serif;
                font-size: 14px;
                border: 2px solid #00d1ff;
                border-radius: 10px;
                padding: 10px;
                white-space: pre-wrap;  /* Ensures formatting like code blocks are preserved */
            }
        """)
        layout.addWidget(self.chat_display)

        # Input field (multi-line)
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00d1ff;
                font-family: 'Arial', sans-serif;
                font-size: 14px;
                border: 2px solid #00d1ff;
                border-radius: 10px;
                padding: 8px 10px;
            }
            QTextEdit:focus {
                border-color: #007acc;
            }
        """)
        self.input_field.setFixedHeight(60)
        self.input_field.installEventFilter(self)  # Install an event filter for key handling
        layout.addWidget(self.input_field)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: #00d1ff;
                font-family: 'Arial', sans-serif;
                font-size: 14px;
                border: 2px solid #00d1ff;
                border-radius: 10px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #007acc;
            }
            QPushButton:pressed {
                background-color: #004e99;
            }
        """)
        self.send_button.clicked.connect(self.handle_message)
        layout.addWidget(self.send_button)

        # Smooth glowing effect
        self.add_glow_effect(self.input_field, QColor(0, 209, 255), 25)
        self.add_glow_effect(self.send_button, QColor(0, 209, 255), 15)

        # Loading animation variables
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.update_loading_message)
        self.loading_state = 0
        self.is_loading = False

    def eventFilter(self, obj, event):
        """Handle custom key press events for the input field."""
        if obj == self.input_field and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return:
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    # Shift+Enter: Add a new line
                    cursor = self.input_field.textCursor()
                    cursor.insertText("\n")
                    return True
                else:
                    # Enter: Send the message
                    self.handle_message()
                    return True
        return super().eventFilter(obj, event)

    def load_messages(self, message_list):
        """Load the message list and display them."""
        self.chat_display.clear()  # Clear existing messages
        for message in message_list:
            role = "You" if message["role"] == "user" else "Bot"
            self.add_message(role, message["content"])

    def handle_message(self):
        """Handle the user input and simulate a bot response with a delay."""
        user_message = self.input_field.toPlainText().strip()
        if user_message:
            # Add user message to the display
            self.add_message("user", user_message)
            self.input_field.clear()

            # Start loading animation
            self.start_loading()

            # Simulate bot response after a delay
            QTimer.singleShot(3000, lambda: self.finish_loading(self.get_bot_response(user_message)))

    def get_bot_response(self, message: str) -> str:
        """Mock bot response logic with Markdown and code syntax."""
        responses = {
            "hello": "Hi there! How can I assist you today?\n\n**Here's some Markdown**:\n\n- **Bold** text\n- *Italic* text\n\n```python\n# Here's some Python code\nprint('Hello, World!')\n```",
            "bye": "Goodbye! Have a great day!",
            "thanks": "You're welcome!"
        }
        return responses.get(message.lower(), "I'm sorry, I don't understand that.")

    def markdown_to_html(self, markdown_text):
        """Convert Markdown to HTML and highlight code."""
        # Use the markdown library to convert the Markdown to HTML
        extensions = [CodeHiliteExtension(linenums=True)]
        html = markdown.markdown(markdown_text, extensions=extensions)

        # Return the HTML formatted response with proper code block wrapping
        return f'<div style="color: #ffffff; font-size: 14px;">{html}</div>'

    def add_glow_effect(self, widget, color, blur_radius):
        """Add a glowing effect to a widget."""
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(blur_radius)
        glow.setColor(color)
        glow.setOffset(0, 0)
        widget.setGraphicsEffect(glow)

    def add_message(self, role: str, content: str):
        """Add a single message to the chat display with proper formatting."""
        if role == "assistant":
            # Render the bot message as HTML (with Markdown formatting)
            formatted_message = f'<p style="color:#00d1ff; font-weight:bold;">Bot:</p><p>{self.markdown_to_html(content)}</p>'
        elif role == "user":
            formatted_message = f'<p style="color:#ffffff; font-weight:bold;">You:</p><p>{content}</p>'
        else:
            formatted_message = f'<p style="color:#808080;">{role}:</p><p>{content}</p>'

        self.chat_display.append(formatted_message)

    def start_loading(self):
        """Start the loading animation."""
        self.is_loading = True
        self.loading_state = 0

        # Add a single placeholder line if none exists yet
        if not self.chat_display.toPlainText().endswith("Bot: "):
            self.add_message("Bot", "")  # Placeholder
        self.loading_timer.start(500)

    def update_loading_message(self):
        """Update the loading animation inline with dots."""
        if self.is_loading:
            self.loading_state = (self.loading_state + 1) % 4
            dots = "." * self.loading_state

            # Move cursor to last line and update with dots
            cursor = self.chat_display.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            cursor.movePosition(cursor.MoveOperation.StartOfBlock, cursor.MoveMode.KeepAnchor)
            cursor.insertText(f"Thinking{dots}", self.chat_display.currentCharFormat())

    def finish_loading(self, bot_response: str):
        """Stop the loading animation and replace the placeholder with the actual response."""
        self.is_loading = False
        self.loading_timer.stop()

        # Replace the last "Bot: " placeholder with the actual response
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.movePosition(cursor.MoveOperation.StartOfBlock, cursor.MoveMode.KeepAnchor)
        cursor.insertText(f"{bot_response}", self.chat_display.currentCharFormat())
    def closeEvent(self, event):
        if self._main_window == None:
            event.accept()
        else:
            self._main_window.setDisabled(False)
            self._main_window.setHidden(False)
            event.accept()
    def configure_on_close(self,self_):
        self._main_window = self_

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatwin = ChatWindow()
    message_list = [
    {"role": "assistant", "content": "Hello, I am a bot!"},
    {"role": "user", "content": "Can you help me?"},
    {"role": "assistant", "content": "Sure! What do you need help with?"}
]
    chatwin.load_messages(message_list)
    chatwin.show()
    sys.exit(app.exec())