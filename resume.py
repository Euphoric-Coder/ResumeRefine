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
        self.font_load(font_path="/fonts/CourierPrime.ttf")

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
        self.jr_label = QLabel("Job Role/Position (JR) ")
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
        # Check if JD or file attachment is missing
        if not self.jdline.toPlainText() or not self.resume:
            self.show_error_message(
                "Error",
                "Please provide both the Job Description (JD) and attach a file.",
            )
            return

        input_prompt = f"""
        You are an expert Resume Reviewer with extensive experience in evaluating resumes for positions in the tech industry, such as Software Engineering, Data Science, Data Analysis, Big Data Engineering, and other related roles. Your task is to:

        1. **Evaluate the Resume**: Analyze the provided resume content against the given job description (JD) and job role (JR).
        2. **Assess Match Percentage**: Assign a percentage score representing how well the resume aligns with the JD, considering relevant skills, experience, and qualifications.
        3. **Rewrite and Enhance**: Rewrite sections of the resume where necessary to better match the job description, improve clarity, impact, and relevancy, and highlight any achievements or skills that should be more prominently featured.
        4. **Provide Constructive Feedback**: Offer specific, actionable suggestions to improve the resume, aiming to increase the JD match to 95% or higher. This could include rephrasing certain sections, adding missing details, or reorganizing the content for better flow.
        5. **Identify Relevant Keywords**: List critical keywords or phrases that are essential for the specific job description and job role. Include a separate section with all the necessary keywords to ensure the resume passes through Applicant Tracking Systems (ATS).
        6. **Suggest Suitable Job Roles**: Based on the resume content, identify and list other job roles or positions for which the candidate is a good fit. Include a separate section titled "Suitable Job Roles" that specifies these roles.
        7. **Provide Tips for Improving JD Match Percentage**: Offer specific tips and strategies to help increase the JD match percentage above 95%. This could include guidance on tailoring specific sections, highlighting certain skills or experiences, and optimizing the use of keywords.
        8. **Generate a Sample Resume**: Based on the improvements suggested, create a sample resume that reflects the necessary changes and optimizations for a better match with the job description.

        **Input Data:**

        - **Resume Content**: {self.resume}
        - **Job Description**: {self.jd}
        - **Job Role**: {self.jr}

        Your response should be structured as follows:

        1. **JD Match Percentage**: Provide a precise percentage match.
        2. **Profile Summary**: Summarize the candidate's profile in a concise and impactful manner.
        3. **Suggested Improvements**: Provide a list of specific improvements to enhance the resume.
        4. **Rewritten Resume Sections**: Rewrite sections of the resume that need improvement.
        5. **Relevant Keywords**: List all keywords relevant to the job description and role, categorizing them into technical skills, soft skills, certifications, etc.
        6. **Additional Keywords for ATS**: A comprehensive list of keywords that should be included to maximize visibility in ATS.
        7. **Suitable Job Roles**: List other job roles or positions that the resume appears to be a good fit for, based on its content.
        8. **Tips for Achieving a JD Match Above 95%**: Provide specific tips and strategies for improving the JD match percentage to above 95%, including suggestions for tailoring, optimizing keywords, and focusing on specific skills or experiences.
        9. **Sample Resume**: Generate a revised sample resume that reflects the suggested changes and optimizations, making it a strong fit for the given job description.

        Aim to provide a detailed, high-quality output that guides the candidate to achieve a JD match of 95% or more and make the resume stand out in a competitive job market.
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

    def show_error_message(self, title, message):
        # Show an error message using QMessageBox
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Icon.Critical)
        error_msg.setWindowTitle(title)
        error_msg.setText(message)
        error_msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and apply stylesheet
    with open("style.css", "r") as file:
        stylesheet = file.read()
    app.setStyleSheet(stylesheet)

    main_window = ResumeReviewer()
    main_window.resize(450, 700)  # Adjust the size of the main window
    main_window.show()
    sys.exit(app.exec())
