# I ACTUALLY KINDA ENJOYED THIS                                                                                                                                                                                                 Def lying
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import time
from threading import Thread

def has_attr(x,y):
    try:
        hasattr(x,y)
        return True
    except:
        return False

class LoginAPIKey(QDialog):
    def __init__(self,platform_name):
        super().__init__()

        self.setWindowTitle(f"Login {platform_name}")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        self.setLayout(layout)

        title = QLabel(f"Login to {platform_name} API")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        self.api_key = None
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter API Key")
        self.api_key_input.setStyleSheet("padding: 5px;")
        layout.addWidget(self.api_key_input)

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
        self._error_d=0

    def handle_submit(self):
        
        self.api_key = self.api_key_input.text().strip()

        # Validation
        if not self.api_key:
            self.show_error_message("Please Enter API Key correctly")
            return
        
        QMessageBox.information(self,"Great","You have done it")

        self.accept()
    def show_error_message(self, message):
        self.error_dialog = QLabel(message)
        self.error_dialog.setStyleSheet("color: red; font-size: 12px;")
        if self._error_d == 0:
            self.central_widget.layout().addWidget(self.error_dialog)
        self._error_d = 1


class LoginCloudFlare(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login CloudFlare")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        self.setLayout(layout)

        title = QLabel("Login to CloudFlare API")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.account_id_input = QLineEdit()
        self.account_id_input.setPlaceholderText("Enter Account ID")
        self.account_id_input.setStyleSheet("padding: 5px;")
        layout.addWidget(self.account_id_input)

        
        self.api_key=None
        self.account_id=None
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter API Key")
        self.api_key_input.setStyleSheet("padding: 5px;")
        layout.addWidget(self.api_key_input)

        

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
        self._error_d=0

    def handle_submit(self):
        
        self.api_key = self.api_key_input.text().strip()
        self.account_id = self.account_id_input.text().strip()

        if not self.api_key or not self.account_id:
            self.show_error_message("Please Enter the Information correctly")
            return
        
        QMessageBox.information(self,"Great","You have done it")
        self.accept()
    def show_error_message(self, message):
        self.error_dialog = QLabel(message)
        self.error_dialog.setStyleSheet("color: red; font-size: 12px;")
        if self._error_d == 0:
            self.central_widget.layout().addWidget(self.error_dialog)
        self._error_d = 1

class DownloadWorker(QThread):
    download_finished = pyqtSignal()
    canceled = pyqtSignal()

    def __init__(self, func_to_call):
        super().__init__()
        self.func_to_call = func_to_call
        self.cancel_requested = False
        self.last_status = ""

    def run(self):
        try:
            self.func_to_call(self)
            if not self.cancel_requested:
                self.download_finished.emit()
        except Exception as e:
            if self.cancel_requested:
                self.canceled.emit()

    def cancel(self):
        self.cancel_requested = True

class WaitingDialog(QDialog):
    def __init__(self,title):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(500, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #2E3440;
                border-radius: 10px;
            }
            QLabel {
                color: #D8DEE9;
                font-size: 14px;
            }
            QPushButton {
                background-color: #81A1C1;
                color: #2E3440;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QPushButton:pressed {
                background-color: #4C566A;
            }
            """
        )

        layout = QVBoxLayout(self)

        self.message_label = QLabel("Please wait while the download completes...", self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.last_status_label = QLabel("Status")
        layout.addWidget(self.message_label)
        layout.addWidget(self.last_status_label)
        self.last_status_label.setStyleSheet("""QLabel {
                color: #66bd63;
                font-size: 12px;
            }""")

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_download)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_spinner)
        self.timer.start(16)
        
        self.worker = None
        self.completion_message = "Download completed."
        self.cancel_message = "Download canceled."
        self.message_box_title = "Download Manager"

    def start_download(self, func_to_call):
        self.worker = DownloadWorker(func_to_call)
        self.worker.download_finished.connect(self.download_complete)
        self.worker.canceled.connect(self.download_canceled)
        self.worker.start()

    def cancel_download(self):
        if self.worker:
            self.worker.cancel()
        self.reject()

    def update_spinner(self):
        self.angle += 5
        if self.angle >= 360:
            self.angle = 0
        self.update()
        self.last_status_label.setText(self.worker.last_status)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        spinner_size = 50
        spinner_x = (self.width() - spinner_size) / 2
        spinner_y = (self.height() - spinner_size) / 2 - 50
        spinner_rect = QRectF(spinner_x, spinner_y, spinner_size, spinner_size)

        pen = QPen(QColor("#81A1C1"))
        pen.setWidth(4)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.save()
        painter.translate(spinner_rect.center())
        painter.rotate(self.angle)
        painter.translate(-spinner_rect.center())

        for i in range(12):
            color = QColor("#81A1C1")
            color.setAlpha(255 - (i * 20))
            pen.setColor(color)
            painter.setPen(pen)
            painter.drawLine(
                QPointF(spinner_rect.center().x(), spinner_rect.top()),
                QPointF(spinner_rect.center().x(), spinner_rect.top() + 10)
            )
            painter.translate(spinner_rect.center())
            painter.rotate(30)
            painter.translate(-spinner_rect.center())

        painter.restore()

    def download_complete(self):
        self.accept()
        QMessageBox.information(self, self.message_box_title, self.completion_message)
        self.close()

    def download_canceled(self):
        QMessageBox.warning(self, self.message_box_title, self.cancel_message)

class PluginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Plugin")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel("Plugin Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.path_label = QLabel("Plugin Path:")
        self.path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_button = QPushButton("Browse...")
        self.path_button.clicked.connect(self.select_file)
        self.path_layout.addWidget(self.path_input)
        self.path_layout.addWidget(self.path_button)
        self.layout.addWidget(self.path_label)
        self.layout.addLayout(self.path_layout)

        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept_data)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

        self.plugin_name = None
        self.plugin_path = None

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Plugin File", "", "ZIP Files (*.zip)")
        if file_path:
            self.path_input.setText(file_path)

    def accept_data(self):
        self.plugin_name = self.name_input.text().strip()
        self.plugin_path = self.path_input.text().strip()

        if not self.plugin_name:
            QMessageBox.warning(self, "Validation Error", "Plugin name cannot be empty.")
            return

        if not self.plugin_path.endswith(".zip"):
            QMessageBox.warning(self, "Validation Error", "Plugin path must point to a .zip file.")
            return

        self.accept()


if __name__ == "__main__": #TEST
    app = QApplication(sys.argv)

    def simulate_download(worker):
        for i in range(50):
            if worker.cancel_requested:
                return
            time.sleep(0.1)

    dialog = WaitingDialog("TESt")
    dialog.start_download(simulate_download)

    if dialog.exec() == QDialog.DialogCode.Rejected:
        print("Download canceled!")
    else:
        print("Download completed!")

    sys.exit(app.exec())
