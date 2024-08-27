import google.generativeai as genai
import PyPDF2 as pdf
import json
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables from the .env file
load_dotenv()

genai.configure(api_key=os.getenv("api_key"))

class ResumeRefine(QDialog):
    def __init__(self):
        super().__init__()

        # Get the primary screen information
        # Get the primary screen information
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # Calculate the center of the screen
        screen_center = screen_geometry.center()

        # Set the window position at the center of the screen
        self.setGeometry(
            screen_center.x() - self.width() // 2,
            screen_center.y() - self.height() // 2,
            200,
            200,
        )

        self.setWindowTitle("Login Window")

        # Create line edits, buttons, and labels
        self.login_edit = QLineEdit(self)
        self.login_edit.setPlaceholderText("Enter the Job Description (optional)")
        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText("Enter your desired Job Role/Position")
        self.add_account_button = QPushButton("Review", self)
        # Create a label for the icon
        self.icon_label = QLabel(self)
        icon_pixmap = QPixmap(
            "./review.png"
        )  # Specify the path to your icon file
        self.icon_label.setPixmap(
            icon_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a label for specific notes
        self.email_notes_label = QLabel(" ", self)
        # self.email_notes_label = QLabel(
        #     "Note: You have to enter your Username that you have created during our Bank's Account Creation on the \nAccounts Section",
        #     self,
        # )

        # Setting the Width of the Line Edits
        line_edit_width = 350
        self.login_edit.setFixedWidth(line_edit_width)
        self.password_edit.setFixedWidth(line_edit_width)
        self.add_account_button.setFixedWidth(300)

        # Create layout for the dialog
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Add icon in its own centered row
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(icon_layout)

        form_layout.addRow("<b>Job Description (JD):</b>", self.login_edit)
        form_layout.addWidget(self.email_notes_label)
        form_layout.addRow("Job Role / Position:", self.password_edit)
        form_layout.addRow(self.add_account_button)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

        # Connect the add account button to the function to add the account
        self.add_account_button.clicked.connect(self.review)

        self.login_edit.setFocus()

    def keyPressEvent(self, event):
        if (
            event.key() == Qt.Key.Key_W
            and event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self.close()
        else:
            super().keyPressEvent(event)

    def review(self):
        pass

    def get_gemini_repsonse(input):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(input)
        return response.text

    def input_pdf_text(uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text


def main():
    # Create the application
    app = QApplication(sys.argv)
    dialog = ResumeRefine()
    dialog.show()

    # Load the QSS style file
    style_file = "style.css"
    with open(style_file, "r") as f:
        style = f.read()

    # Apply the style to the application
    app.setStyleSheet(style)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     print(get_gemini_repsonse("what is the difference between cse and cs degree? Explain a bit in detail!"))
