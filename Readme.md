# PDFLIFY
## Project Description

PDFLIFY is a web-based file conversion tool designed to effortlessly transform PDF documents into `.docx` (Microsoft Word) or `.txt` (plain text) formats. While the core backend logic handles robust file processing, the primary focus of this project's recent revamp has been on delivering a highly interactive, modern, and visually engaging user interface. This transformation aims to showcase strong front-end development skills, attention to detail, and a commitment to exceptional user experience.

## Features

* **PDF to DOCX Conversion:** Convert PDF files into editable Microsoft Word documents.
* **PDF to TXT Conversion:** Extract plain text content from PDF files.
* **Sleek & Modern UI:** A professional dark-mode aesthetic with a vibrant accent color, designed for visual appeal.
* **Intuitive Drag-and-Drop:** Easily upload files via a prominent drag-and-drop interface.

## Technologies Used

* **Backend:** Python (Flask)
* **Frontend:**
    * HTML5
    * CSS3 (Custom, modern design)
    * JavaScript (for UI interactions)
* **File Conversion Library:** (Implicit, assuming a Python library like `pdf2docx` or `PyPDF2` combined with `python-docx` would be used in the Flask backend)

## Installation and Setup

To get this project up and running locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd SleekConverter
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install Flask python-docx pdf2docx # Example libraries, adjust as per your actual backend
    ```
    *Note: Replace `python-docx` and `pdf2docx` with the actual libraries your Flask backend uses for PDF processing and DOCX creation.*

4.  **Run the Application:**
    ```bash
    export FLASK_APP=app.py # Assuming your main Flask file is `app.py`
    flask run
    ```
    (On Windows, you might use `set FLASK_APP=app.py`)

    The application will typically be available at `http://127.0.0.1:5000/`.

## Usage

1.  Navigate to the application in your web browser.
2.  Drag and drop your PDF file into the designated upload area, or click "Browse Files" to select one.
3.  Choose your desired output format (DOCX or TXT).
4.  Click the "Convert Now" button.
5.  (Assuming your backend handles download) Your converted file will be downloaded automatically.

## Project Structure
├── app.py                  # Flask backend application logic
├── static/
│   ├── css/
│   │   └── style.css       # Custom modern CSS for the UI
│   └── js/
│       └── main.js         # (Optional) For more complex JS interactions
├── templates/
│   └── index.html          # Main application interface
├── venv/                   # Python virtual environment
├── README.md               # Project README file
└── requirements.txt        # Python dependencies