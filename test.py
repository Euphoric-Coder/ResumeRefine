from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFontDatabase
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Load the font
        self.font_load()

        # Set up the UI
        self.init_ui()

    def font_load(self, font_path="./fonts/GloriaHallelujah.ttf"):
        # Convert to absolute path for clarity
        font_path = os.path.abspath(font_path)

        # Check if the font file exists
        if not os.path.exists(font_path):
            print(f"Font file not found at path: {font_path}")
            return False

        # Attempt to add the font to the application
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id != -1:
            loaded_fonts = QFontDatabase.applicationFontFamilies(font_id)
            print(f"Font loaded successfully: {loaded_fonts}")
            return True
        else:
            print(f"Failed to load font from path: {font_path}")
            return False

    def init_ui(self):
        # Create a label
        self.label = QLabel("Hello, PyQt6 with Custom Font!")
        self.label.setObjectName("customLabel")  # Set an object name for CSS targeting

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("Custom Font with PyQt6")
        self.resize(400, 200)

        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        # Load the CSS file
        stylesheet_path = os.path.abspath("./style.css")  # Adjust the path accordingly
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Stylesheet file not found at path: {stylesheet_path}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
