import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QFontDatabase

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/YourCustomFont.ttf")
    if font_id == -1:
        print("Error: Font not loaded.")
        sys.exit(-1)

    # Get the font family name
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        font_family = font_families[0]

        # Use the custom font
        custom_font = QFont(font_family)
        label = QLabel("Hello, World!")
        label.setFont(custom_font)
        label.show()

    sys.exit(app.exec_())
