import google.generativeai as genai
import PyPDF2 as pdf
import json
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

genai.configure(api_key=os.getenv("api_key"))

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFileDialog,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ResumeReviewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resume Reviewer")

        # Set the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Icon and title
        icon_layout = QHBoxLayout()
        icon = QLabel(self)
        # Load and set the image file for the icon
        pixmap = QPixmap("./review.png")  # Replace with your image path
        icon.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon)
        layout.addLayout(icon_layout)

        # Job description
        self.job_description_edit = QLineEdit()
        self.job_description_edit.setPlaceholderText("Enter job description")
        layout.addWidget(self.job_description_edit)

        # Job role/position
        self.job_role_edit = QLineEdit()
        self.job_role_edit.setPlaceholderText("Enter job role/position")
        layout.addWidget(self.job_role_edit)

        # Review button
        review_button = QPushButton("Review")
        review_button.clicked.connect(self.on_review_button_clicked)
        layout.addWidget(review_button)

        # File dialog button
        file_button = QPushButton("Choose File")
        file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(file_button)

        # Disabled text edit (initially hidden)
        self.result_edit = QTextEdit()
        self.result_edit.setVisible(False)
        layout.addWidget(self.result_edit)

    def on_review_button_clicked(self):
        # Toggle visibility of the QTextEdit
        if not self.result_edit.isVisible():
            self.result_edit.setVisible(True)
            self.result_edit.setText("hello")

    def open_file_dialog(self):
        # Open a file dialog to choose a file
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                # Hide the QTextEdit if a file is selected
                self.result_edit.setVisible(False)

    def get_gemini_repsonse(self, input):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(input)
        return response.text

    def input_pdf_text(self, uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and apply stylesheet
    with open("style.css", "r") as file:
        stylesheet = file.read()
    app.setStyleSheet(stylesheet)

    main_window = ResumeReviewer()
    main_window.resize(400, 300)  # Adjust the size of the main window
    main_window.show()
    sys.exit(app.exec())


