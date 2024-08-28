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


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


class ResumeReviewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ResumeRefine")
        # Loads the External Google Fonts
        self.font_load(font_path="./fonts/Raleway.ttf")
        self.font_load(font_path="./fonts/Caveat.ttf")

        # Set the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.jd = ""
        self.resume = ""
        self.jr = ""
        # Icon and title
        icon_layout = QHBoxLayout()
        icon = QLabel(self)

        # Load and set the image file for the icon
        pixmap = QPixmap("./assets/review.png")  # Replace with your image path
        icon.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name = QLabel("ResumeRefine")
        self.name.setObjectName("appname")
        layout.addLayout(icon_layout)
        icon_layout.addWidget(icon)
        icon_layout.addWidget(self.name)

        # Job description
        job_description = QHBoxLayout()
        self.jd_label = QLabel("Job Description (JD) ")
        # job_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.jdline = QTextEdit()
        self.jdline.setFixedHeight(100)
        self.jdline.setObjectName("jdline")
        self.jd_label.setObjectName("jd")
        layout.addLayout(job_description)
        job_description.addWidget(self.jd_label)
        job_description.addWidget(self.jdline)

        # Job role/position
        job_role = QHBoxLayout()
        self.jr_label = QLabel("Job Role / Position (JR) ")
        # job_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.jr_line = QLineEdit()
        self.jr_line.setObjectName("jrline")
        self.jr_label.setObjectName("jr")
        layout.addLayout(job_role)
        job_role.addWidget(self.jr_label)
        job_role.addWidget(self.jr_line)

        # Review button
        review_button = QPushButton("Review")
        review_button.clicked.connect(self.on_review_button_clicked)

        # File dialog button
        file_button = QPushButton("Choose File")
        file_button.clicked.connect(self.open_file_dialog)

        # Disabled text edit (initially hidden)
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)

        layout.addWidget(file_button)
        layout.addWidget(review_button)
        layout.addWidget(self.result_edit)

    def on_review_button_clicked(self):
        input_prompt = f"""
        Act Like a very skilled or experienced Resume Reviewer
        with a deep understanding of tech field,software engineering, data science, data analyst,
        big data engineer and many other position. Your task is to evaluate the resume based on the given 
        job description. You must consider the job market is very competitive and you should provide
        best assistance for improving the resumes. Assign the percentage Matching based
        on JD and a summary of the resume profile and
        the suggestions to improve the resume with high accuracy
        Resume:{self.resume}
        Job Description:{self.jd}
        Job Role: {self.jr}

        Also mention the JD Match in percentage.
        Give a in detail explanation what could be done to make the resume more good. 
        Show a modified resume also using the same data.
        Also mention the relevant keywords that are needed for this job.
        """
        # I want the response in one single string having the structure
        # {{"JD Match":"%","Profile Summary":"", "Suggestions:[]"}}
        # Toggle visibility of the QTextEdit
        self.result_edit.setText(self.get_gemini_repsonse(input=input_prompt))

    def open_file_dialog(self):
        # Open a file dialog to choose a file
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            print(selected_files)
            if selected_files:
                # Hide the QTextEdit if a file is selected
                self.result_edit.setText("")
                self.resume = "\n" + input_pdf_text(uploaded_file=selected_files[0])
                self.jd = self.jdline.toPlainText()
                self.jr = self.jr_line.text()

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

    def font_load(self, font_path="./fonts/Poppins.ttf"):
        # Convert to absolute path for clarity
        font_path = os.path.abspath(font_path)

        # Check if the font file exists
        if not os.path.exists(font_path):
            return False

        # Attempt to add the font to the application
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id != -1:
            return True
        else:
            return False


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
