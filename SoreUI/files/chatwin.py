from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

class ChatMessageWidget(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOpenLinks(False)
        self.setMinimumWidth(600)
        self.setMaximumWidth(600)
        self.document().setDocumentMargin(10)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_styles()
        self.setup_connections()
        self.loading_state = 0
        self.is_loading = False
        self._main_window = None

    def setup_ui(self):
        self.setWindowTitle("OMEGAPy-Xero Chat")
        self.resize(800, 600)
        self.setMinimumSize(400, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Chat history
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setContentsMargins(0, 0, 10, 0)
        self.chat_layout.setSpacing(15)
        self.chat_scroll.setWidget(self.chat_container)
        main_layout.addWidget(self.chat_scroll)

        # Input area
        input_container = QWidget()
        input_container.setMaximumHeight(100)
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)
        

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.setMinimumHeight(60)
        input_layout.addWidget(self.input_field, 1)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(80, 60)
        input_layout.addWidget(self.send_button)

        main_layout.addWidget(input_container)

        # Loading indicator
        self.loading_indicator = QLabel()
        self.loading_indicator.hide()
        main_layout.addWidget(self.loading_indicator)

        # Scroll timer
        self.scroll_timer = QTimer()
        self.scroll_timer.setInterval(100)
        self.scroll_timer.timeout.connect(self.ensure_scroll)
        QShortcut(QKeySequence(Qt.Key.Key_Down), self, self.ensure_scroll)
        QShortcut(QKeySequence("Ctrl+X"), self, self.clear_chat)
        
        

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QScrollArea {
                border: none;
                background-color: #1a1a1a;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                padding: 1px;
                font-family: 'Segoe UI';
                font-size: 14px;
                selection-background-color: #3a6da4;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                padding: 8px 16px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
        """)

        self.loading_indicator.setStyleSheet("""
            QLabel {
                color: #4d4d4d;
                font-family: 'Segoe UI';
                font-size: 12px;
                qproperty-alignment: AlignCenter;
            }
        """)

    def setup_connections(self):
        self.send_button.clicked.connect(self.send_message)
        self.input_field.installEventFilter(self)
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.update_loading)

    def eventFilter(self, obj, event):
        if obj == self.input_field and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)

    def create_message_bubble(self, message, is_user=False):
        bubble = ChatMessageWidget()
        bubble.setHtml(self.format_message(message, is_user))
        bubble.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {'#2d5a7c' if is_user else '#2d2d2d'};
                color: #ffffff;
                border-radius: 12px;
                border: 1px solid {'#3a6da4' if is_user else '#3d3d3d'};
            }}
        """)
        return bubble

    def format_message(self, text, is_user=False):
        if not is_user:
            text = markdown.markdown(text, extensions=[CodeHiliteExtension(noclasses=True)])
        return f"""
            <div style="font-family: 'Segoe UI'; font-size: 14px; line-height: 1.4;">
                {text}
            </div>
        """

    def send_message(self):
        message = self.input_field.toPlainText().strip()
        if not message:
            return

        self.input_field.clear()
        self.add_message(message, is_user=True)
        self.start_loading()
        QTimer.singleShot(1500, lambda: self.receive_message("Here's a sample response with **Markdown** and `code`."))

    def add_message(self, message, is_user=False):
        bubble = self.create_message_bubble(message, is_user)
        self.chat_layout.addWidget(bubble, alignment=Qt.AlignmentFlag.AlignRight if is_user else Qt.AlignmentFlag.AlignLeft)
        self.scroll_timer.start()
    
    def ensure_scroll(self):
        self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        )
        self.scroll_timer.stop()

    def start_loading(self):
        self.is_loading = True
        self.loading_timer.start(500)
        self.loading_indicator.show()

    def update_loading(self):
        self.loading_state = (self.loading_state + 1) % 4
        dots = "." * self.loading_state
        self.loading_indicator.setText(f"Bot is thinking{dots}")

    def receive_message(self, message):
        self.is_loading = False
        self.loading_timer.stop()
        self.loading_indicator.hide()
        self.add_message(message, is_user=False)
    def clear_chat(self):
        for i in reversed(range(self.chat_layout.count())):
            self.chat_layout.itemAt(i).widget().deleteLater()

    def closeEvent(self, event):
        if self._main_window:
            self._main_window.setDisabled(False)
            self._main_window.setHidden(False)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())