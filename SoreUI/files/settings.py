from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import json



class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setMaximumSize(600, 500)
        self.setBaseSize(600,500)
        self.settings = {"General": {}, "API Settings": {}, "Security": {}, "Chat Settings": {}, "About Us": {}}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 600, 400)
        
        # Main layout
        main_layout = QHBoxLayout()

        # List widget for rows
        self.row_list = QListWidget()
        self.row_list.addItems(["General", "API Settings", "Security", "Chat Settings", "About Us"])
        self.row_list.setFixedWidth(150)
        main_layout.addWidget(self.row_list)

        # Settings area
        self.settings_area = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_area)
        self.settings_area.setLayout(self.settings_layout)
        main_layout.addWidget(self.settings_area)

        # Set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect signals
        self.row_list.currentRowChanged.connect(self.display_row)


    def init_general_tab(self):
        """Create General tab."""
        general_tab = QWidget()
        layout = QVBoxLayout(general_tab)

        # Style Section
        layout.addWidget(QLabel("Style Section:"))

        # Background Image
        self.background_image = QPushButton("Select Background Image")
        self.background_image.clicked.connect(lambda: self.select_file("Background_image"))
        layout.addWidget(self.background_image)

        # Main Button Background
        self.main_button_bg = QPushButton("Select Main Button Background Image")
        self.main_button_bg.clicked.connect(lambda: self.select_file("Main_button_background"))
        layout.addWidget(self.main_button_bg)

        # Primary Color
        self.primary_color = QPushButton("Select Primary Color")
        self.primary_color.clicked.connect(lambda: self.select_color("PrimaryColor"))
        layout.addWidget(self.primary_color)

        # Secondary Color
        self.secondary_color = QPushButton("Select Secondary Color")
        self.secondary_color.clicked.connect(lambda: self.select_color("SecondaryColor"))
        layout.addWidget(self.secondary_color)

        # Fixed Size
        fixed_size_layout = QHBoxLayout()
        self.fixed_width = QSpinBox()
        self.fixed_width.setRange(0, 1920)
        self.fixed_height = QSpinBox()
        self.fixed_height.setRange(0, 1080)
        fixed_size_layout.addWidget(QLabel("Fixed Width:"))
        fixed_size_layout.addWidget(self.fixed_width)
        fixed_size_layout.addWidget(QLabel("Fixed Height:"))
        fixed_size_layout.addWidget(self.fixed_height)
        layout.addLayout(fixed_size_layout)

        # Additional CSS
        self.additional_css = QTextEdit()
        self.additional_css.setPlaceholderText("Enter additional CSS here...")
        layout.addWidget(QLabel("Additional CSS:"))
        layout.addWidget(self.additional_css)

        self.stacked_widget.addWidget(general_tab)

    def init_api_tab(self):
        """Create API Settings tab."""
        api_tab = QWidget()
        layout = QVBoxLayout(api_tab)

        # Default API Section
        layout.addWidget(QLabel("Default API Section:"))

        # Select API Dropdown
        self.select_api = QComboBox()
        self.select_api.addItems(["None", "API1", "API2", "API3"])
        layout.addWidget(self.select_api)

        # API Key Input
        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("Enter API key...")
        self.api_key.setEnabled(False)
        self.select_api.currentIndexChanged.connect(self.toggle_api_key)
        layout.addWidget(self.api_key)

        # Train-on Section
        layout.addWidget(QLabel("Train-on Section:"))

        # Train Format Dropdown
        self.train_format = QComboBox()
        self.train_format.addItems(["Default", "Custom Format 1", "Custom Format 2"])
        layout.addWidget(self.train_format)

        # Additional Command
        self.additional_command = QLineEdit()
        self.additional_command.setPlaceholderText("Enter additional command...")
        layout.addWidget(QLabel("Additional Command:"))
        layout.addWidget(self.additional_command)

        # Libraries Section
        layout.addWidget(QLabel("Libraries to Import:"))
        self.libraries_list = QListWidget()
        layout.addWidget(self.libraries_list)
        library_controls = QHBoxLayout()
        add_library = QPushButton("Add")
        add_library.clicked.connect(self.add_library)
        remove_library = QPushButton("Remove")
        remove_library.clicked.connect(self.remove_library)
        library_controls.addWidget(add_library)
        library_controls.addWidget(remove_library)
        layout.addLayout(library_controls)

        self.stacked_widget.addWidget(api_tab)

    def init_security_tab(self):
        """Create Security tab."""
        security_tab = QWidget()
        layout = QVBoxLayout(security_tab)

        # Security Mode Section
        layout.addWidget(QLabel("Security Mode Section:"))

        # Select Security Method
        self.security_method = QComboBox()
        self.security_method.addItems(["Password", "FaceLock"])
        self.security_method.currentIndexChanged.connect(self.toggle_security_options)
        layout.addWidget(self.security_method)

        # Security Options
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password...")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setVisible(True)
        layout.addWidget(self.password_input)

        self.face_analyze_button = QPushButton("Analyze Face")
        self.face_check_button = QPushButton("Check Face")
        self.face_analyze_button.setVisible(False)
        self.face_check_button.setVisible(False)
        layout.addWidget(self.face_analyze_button)
        layout.addWidget(self.face_check_button)

        self.stacked_widget.addWidget(security_tab)

    def init_chat_settings_tab(self):
        """Create Chat Settings tab."""
        chat_tab = QWidget()
        layout = QVBoxLayout(chat_tab)

        # Chat Style Section
        layout.addWidget(QLabel("Chat Style Section:"))

        # Primary Color
        self.chat_primary_color = QPushButton("Select Primary Color")
        self.chat_primary_color.clicked.connect(lambda: self.select_color("ChatPrimaryColor"))
        layout.addWidget(self.chat_primary_color)

        # Secondary Color
        self.chat_secondary_color = QPushButton("Select Secondary Color")
        self.chat_secondary_color.clicked.connect(lambda: self.select_color("ChatSecondaryColor"))
        layout.addWidget(self.chat_secondary_color)

        # Font Selection
        self.font_button = QPushButton("Select Font")
        self.font_button.clicked.connect(self.select_font)
        layout.addWidget(self.font_button)

        # Additional CSS
        self.chat_css = QTextEdit()
        self.chat_css.setPlaceholderText("Enter chat additional CSS here...")
        layout.addWidget(QLabel("Additional CSS:"))
        layout.addWidget(self.chat_css)

        self.stacked_widget.addWidget(chat_tab)

    def init_about_us_tab(self):
        """Create About Us tab."""
        about_tab = QWidget()
        layout = QVBoxLayout(about_tab)

        # About Us Section
        layout.addWidget(QLabel("About Us Section"))
        layout.addWidget(QLabel("This is an application created by ExampleCorp."))

        # Social Media Section
        social_media_layout = QHBoxLayout()
        layout.addWidget(QLabel("Social Media Section"))
        facebook_button = QPushButton("Facebook")
        twitter_button = QPushButton("Twitter")
        linkedin_button = QPushButton("LinkedIn")
        social_media_layout.addWidget(facebook_button)
        social_media_layout.addWidget(twitter_button)
        social_media_layout.addWidget(linkedin_button)
        layout.addLayout(social_media_layout)

        self.stacked_widget.addWidget(about_tab)

    def select_file(self, key):
        """Open file dialog to select a file."""
        file, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file:
            self.settings["General"][key] = file

    def select_color(self, key):
        """Open color dialog to select a color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.settings["General"][key] = color.name()

    def select_font(self):
        """Open font dialog to select a font."""
        font, ok = QFontDialog.getFont()
        if ok:
            self.settings["Chat Settings"]["Font"] = font.toString()

    def toggle_api_key(self):
        """Enable or disable API key input."""
        self.api_key.setEnabled(self.select_api.currentText() != "None")

    def add_library(self):
        """Add a library to the list."""
        item, ok = QInputDialog.getText(self, "Add Library", "Enter library name:")
        if ok and item:
            self.libraries_list.addItem(item)

    def remove_library(self):
        """Remove selected library from the list."""
        for item in self.libraries_list.selectedItems():
            self.libraries_list.takeItem(self.libraries_list.row(item))
    def toggle_security_options(self):
            """Toggle visibility of security options based on selected method."""
            method = self.security_method.currentText()
            if method == "Password":
                self.password_input.setVisible(True)
                self.face_analyze_button.setVisible(False)
                self.face_check_button.setVisible(False)
            elif method == "FaceLock":
                self.password_input.setVisible(False)
                self.face_analyze_button.setVisible(True)
                self.face_check_button.setVisible(True)

    def save_settings(self):
        """Save the settings to a file."""
        settings = {}

        # General Settings (example)
        settings["General"] = {
            "AdditionalCss": self.additional_css.toPlainText() if hasattr(self, 'additional_css') else "",
            "FixedWidth": self.fixed_width.value() if hasattr(self, 'fixed_width') else 0,
            "FixedHeight": self.fixed_height.value() if hasattr(self, 'fixed_height') else 0,
        }

        # API Settings (example)
        if hasattr(self, 'select_api'):
            settings["API Settings"] = {
                "SelectedAPI": self.select_api.currentText() if self.select_api.currentIndex() >= 0 else "",
                "ApiKey": self.select_api_key.text() if hasattr(self, 'select_api_key') else "",
                "TrainFormat": self.train_format.currentText() if hasattr(self, 'train_format') else "",
                "AdditionalCommand": self.additional_command.text() if hasattr(self, 'additional_command') else "",
                "Libraries": [self.libraries_list.item(i).text() for i in range(self.libraries_list.count())] if hasattr(self, 'libraries_list') else []
            }

        # Security Settings (similar check for each section)
        # Repeat for other sections like Chat Settings, Security, etc.

        # Save to a JSON file
        with open("settings.json", "w") as file:
            json.dump(settings, file, indent=4)

    def display_row(self, index):
        """Displays the appropriate settings for the selected row."""
        # Clear the settings layout
        while self.settings_layout.count():
            child = self.settings_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Populate settings based on the selected row
        if index == 0:  # General
            self.add_general_settings()
        elif index == 1:  # API Settings
            self.add_api_settings()
        elif index == 2:  # Security
            self.add_security_settings()
        elif index == 3:  # Chat Settings
            self.add_chat_settings()
        elif index == 4:  # About Us
            self.add_about_us()
    def add_general_settings(self):
        """Add widgets for the 'General' settings tab."""
        # Clear existing widgets
        for i in reversed(range(self.settings_layout.count())):
            widget = self.settings_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()

        # Style Section
        background_image_label = QLabel("Background Image:")
        background_image_button = QPushButton("Choose File")

        # Main Button Section
        main_button_bg_label = QLabel("Main Button Background Image:")
        main_button_bg_button = QPushButton("Choose File")

        # Primary Color
        primary_color_label = QLabel("Primary Color:")
        primary_color_button = QPushButton("Select Color")

        # Secondary Color
        secondary_color_label = QLabel("Secondary Color:")
        secondary_color_button = QPushButton("Select Color")

        # Fixed Size Inputs
        fixed_size_label = QLabel("Fixed Size (Width x Height):")
        self.fixed_width = QSpinBox()  # Create QSpinBox for width
        self.fixed_width.setRange(0, 9999)  # Set range for width
        self.fixed_height = QSpinBox()  # Create QSpinBox for height
        self.fixed_height.setRange(0, 9999)  # Set range for height

        # Additional CSS
        additional_css_label = QLabel("Additional CSS:")
        self.additional_css = QTextEdit()  # Initialize QTextEdit widget for Additional CSS

        # Save Changes Button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_settings)

        # Add widgets to the layout
        self.settings_layout.addWidget(background_image_label)
        self.settings_layout.addWidget(background_image_button)
        self.settings_layout.addWidget(main_button_bg_label)
        self.settings_layout.addWidget(main_button_bg_button)
        self.settings_layout.addWidget(primary_color_label)
        self.settings_layout.addWidget(primary_color_button)
        self.settings_layout.addWidget(secondary_color_label)
        self.settings_layout.addWidget(secondary_color_button)
        self.settings_layout.addWidget(fixed_size_label)
        self.settings_layout.addWidget(self.fixed_width)
        self.settings_layout.addWidget(self.fixed_height)
        self.settings_layout.addWidget(additional_css_label)
        self.settings_layout.addWidget(self.additional_css)
        self.settings_layout.addWidget(save_button)


    def add_api_settings(self):
        """Add widgets for the 'API Settings' tab."""
        # Clear existing widgets
        for i in reversed(range(self.settings_layout.count())):
            widget = self.settings_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()

        # Default API Section
        api_label = QLabel("Select API:")
        self.select_api = QComboBox()  # Create a combo box for API selection
        self.select_api.addItems(["API 1", "API 2", "API 3"])  # Populate with API options

        api_key_label = QLabel("API Key:")
        self.select_api_key = QLineEdit()  # API key input box (initially empty)

        # Train-on Section
        train_format_label = QLabel("Train Format:")
        self.train_format = QComboBox()  # Dropdown menu for train format
        self.train_format.addItems(["Format 1", "Format 2", "Format 3"])  # Example formats

        additional_command_label = QLabel("Additional Command:")
        self.additional_command = QLineEdit()  # Input for additional command (initially empty)

        # Libraries to import Section
        libraries_label = QLabel("Libraries to Import:")
        self.libraries_list = QListWidget()  # List widget for libraries
        self.libraries_list.addItem("Library 1")  # Example library
        self.libraries_list.addItem("Library 2")

        # Save Changes Button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_settings)

        # Add widgets to the layout
        self.settings_layout.addWidget(api_label)
        self.settings_layout.addWidget(self.select_api)
        self.settings_layout.addWidget(api_key_label)
        self.settings_layout.addWidget(self.select_api_key)
        self.settings_layout.addWidget(train_format_label)
        self.settings_layout.addWidget(self.train_format)
        self.settings_layout.addWidget(additional_command_label)
        self.settings_layout.addWidget(self.additional_command)
        self.settings_layout.addWidget(libraries_label)
        self.settings_layout.addWidget(self.libraries_list)
        self.settings_layout.addWidget(save_button)


    def add_security_settings(self):
        """Add widgets for the 'Security' settings."""
        # Clear any existing widgets
        for i in reversed(range(self.settings_layout.count())):
            widget = self.settings_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()

        # Security mode section
        security_mode_label = QLabel("Select Security Method:")
        security_mode_dropdown = QComboBox()
        security_mode_dropdown.addItems(["Password", "FaceLock"])

        # Security options section
        password_label = QLabel("Password:")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)

        face_analyze_button = QPushButton("Face Analyze")
        face_check_button = QPushButton("Face Check")

        # Stack widgets based on selected security method
        password_widget = QWidget()
        password_layout = QVBoxLayout()
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_input)
        password_widget.setLayout(password_layout)

        facelock_widget = QWidget()
        facelock_layout = QVBoxLayout()
        facelock_layout.addWidget(face_analyze_button)
        facelock_layout.addWidget(face_check_button)
        facelock_widget.setLayout(facelock_layout)

        security_stack = QStackedWidget()
        security_stack.addWidget(password_widget)
        security_stack.addWidget(facelock_widget)

        # Update the stack when the dropdown value changes
        def update_security_stack(index):
            security_stack.setCurrentIndex(index)

        security_mode_dropdown.currentIndexChanged.connect(update_security_stack)

        # Save button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_settings)

        # Add widgets to the layout
        self.settings_layout.addWidget(security_mode_label)
        self.settings_layout.addWidget(security_mode_dropdown)
        self.settings_layout.addWidget(security_stack)
        self.settings_layout.addWidget(save_button)
    def add_chat_settings(self):
        """Add widgets for the 'Chat Settings' tab."""
        # Clear existing widgets
        for i in reversed(range(self.settings_layout.count())):
            widget = self.settings_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()

        # Chat Style Section
        primary_color_label = QLabel("Primary Color:")
        primary_color_picker = QPushButton("Choose Color")
        primary_color_picker.clicked.connect(lambda: self.choose_color("primary_color"))

        secondary_color_label = QLabel("Secondary Color:")
        secondary_color_picker = QPushButton("Choose Color")
        secondary_color_picker.clicked.connect(lambda: self.choose_color("secondary_color"))

        font_label = QLabel("Font:")
        font_input = QFontComboBox()

        additional_css_label = QLabel("Additional CSS:")
        additional_css_input = QTextEdit()

        # Save button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_settings)

        # Add widgets to the layout
        self.settings_layout.addWidget(primary_color_label)
        self.settings_layout.addWidget(primary_color_picker)
        self.settings_layout.addWidget(secondary_color_label)
        self.settings_layout.addWidget(secondary_color_picker)
        self.settings_layout.addWidget(font_label)
        self.settings_layout.addWidget(font_input)
        self.settings_layout.addWidget(additional_css_label)
        self.settings_layout.addWidget(additional_css_input)
        self.settings_layout.addWidget(save_button)

    def choose_color(self, setting_name):
        """Open a color picker and update the setting."""
        color = QColorDialog.getColor()
        if color.isValid():
            # Save or apply the chosen color as needed
            print(f"{setting_name} chosen: {color.name()}")
    def add_about_us(self):
        """Add widgets for the 'About Us' tab."""
        # Clear existing widgets
        for i in reversed(range(self.settings_layout.count())):
            widget = self.settings_layout.takeAt(i).widget()
            if widget:
                widget.deleteLater()

        # About Us Section
        about_us_label = QLabel("About Us:")
        about_us_text = QTextEdit()
        about_us_text.setText("Your text for the About Us section goes here.")
        
        # Social Media Section
        social_media_label = QLabel("Social Media Links:")
        twitter_button = QPushButton("Twitter")
        facebook_button = QPushButton("Facebook")
        instagram_button = QPushButton("Instagram")

        # Layout for Social Media Buttons
        social_layout = QHBoxLayout()
        social_layout.addWidget(twitter_button)
        social_layout.addWidget(facebook_button)
        social_layout.addWidget(instagram_button)

        # Save button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_settings)

        # Add widgets to the layout
        self.settings_layout.addWidget(about_us_label)
        self.settings_layout.addWidget(about_us_text)
        self.settings_layout.addWidget(social_media_label)
        self.settings_layout.addLayout(social_layout)
        self.settings_layout.addWidget(save_button)





if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    settings_window = SettingsWindow()
    settings_window.show()
    sys.exit(app.exec())