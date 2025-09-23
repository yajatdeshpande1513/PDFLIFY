from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from pdf2docx import Converter
import pdfplumber
import io
import zipfile
from werkzeug.security import generate_password_hash, check_password_hash
import shutil # For deleting directories

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # Change this to a strong, random key
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CONVERTED_FOLDER'] = 'converted'

# Ensure upload and converted folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to login page if not authenticated

# --- User Management (for demonstration, in-memory dictionary) ---
users = {} # Stores {'username': {'password_hash': '...', 'id': '...'}}
user_id_counter = 0

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    for username, user_data in users.items():
        if str(user_data['id']) == user_id:
            return User(user_data['id'], username)
    return None

# --- Routes ---

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/tools', methods=['GET'])
@login_required # Only logged-in users can access tools
def tools():
    return render_template('tools.html')

# Placeholder routes for specific tools
@app.route('/tools/audio')
@login_required
def audio_converter():
    flash("Audio Converter is under development!", "info")
    return render_template('tools.html')

@app.route('/tools/video')
@login_required
def video_converter():
    flash("Video Converter is under development!", "info")
    return render_template('tools.html')

@app.route('/tools/font')
@login_required
def font_converter():
    flash("Font Converter is under development!", "info")
    return render_template('tools.html')

@app.route('/tools/archive')
@login_required
def archive_converter():
    flash("Archive Converter is under development!", "info")
    return render_template('tools.html')

@app.route('/tools/ebook')
@login_required
def ebook_converter():
    flash("Ebook Converter is under development!", "info")
    return render_template('tools.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('signup'))

        if username in users:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))

        global user_id_counter
        user_id_counter += 1
        hashed_password = generate_password_hash(password)
        users[username] = {'password_hash': hashed_password, 'id': user_id_counter}
        
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = users.get(username)
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], username)
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('index'))

    if file and file.filename.endswith('.pdf'):
        # Create a unique subdirectory for each conversion to manage files
        conversion_id = os.urandom(8).hex()
        temp_dir = os.path.join(app.config['CONVERTED_FOLDER'], conversion_id)
        os.makedirs(temp_dir, exist_ok=True)

        input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_pdf_path)

        output_formats = request.form.getlist('output_format')
        
        converted_files = []
        
        if 'docx' in output_formats:
            output_word_filename = file.filename.replace('.pdf', '.docx')
            output_word_path = os.path.join(temp_dir, output_word_filename)
            try:
                cv = Converter(input_pdf_path)
                cv.convert(output_word_path)
                cv.close()
                converted_files.append(output_word_path)
            except Exception as e:
                flash(f"Error converting to DOCX: {e}", "danger")

        if 'txt' in output_formats:
            output_text_filename = file.filename.replace('.pdf', '.txt')
            output_text_path = os.path.join(temp_dir, output_text_filename)
            try:
                with pdfplumber.open(input_pdf_path) as pdf:
                    text = ''
                    for page in pdf.pages:
                        text += page.extract_text() if page.extract_text() else ''
                with open(output_text_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                converted_files.append(output_text_path)
            except Exception as e:
                flash(f"Error converting to TXT: {e}", "danger")

        # Clean up the original uploaded PDF
        os.remove(input_pdf_path)

        if not converted_files:
            flash("No output format selected or conversion failed.", "danger")
            shutil.rmtree(temp_dir) # Clean up empty temp directory
            return redirect(url_for('index'))

        if len(converted_files) == 1:
            # If only one file, send it directly
            return send_file(converted_files[0], as_attachment=True, download_name=os.path.basename(converted_files[0]))
        else:
            # If multiple files, zip them
            zip_filename = f"{file.filename.replace('.pdf', '')}_converted.zip"
            zip_path = os.path.join(app.config['CONVERTED_FOLDER'], zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zf:
                for cf in converted_files:
                    zf.write(cf, os.path.basename(cf))
            
            # Clean up individual converted files and their temp directory
            shutil.rmtree(temp_dir)

            return send_file(zip_path, as_attachment=True, download_name=zip_filename)

    flash('Invalid file type. Please upload a PDF.', 'danger')
    return redirect(url_for('index'))

# Cleanup for converted zip files after they are sent (optional, can be done by a background task)
@app.after_request
def cleanup_files(response):
    if request.path == url_for('convert') and request.method == 'POST':
        # This is a simplistic cleanup. In a real app, use a background task
        # or a more robust file management strategy.
        # For now, we'll just delete the zip file if it was created.
        if 'download_name' in response.headers and response.headers['download_name'].endswith('.zip'):
            zip_path = os.path.join(app.config['CONVERTED_FOLDER'], response.headers['download_name'])
            if os.path.exists(zip_path):
                os.remove(zip_path)
    return response


if __name__ == '__main__':
    app.run(debug=True)