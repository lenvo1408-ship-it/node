import os
from flask import Flask, request, redirect, render_template_string, send_from_directory, session

UPLOAD_FOLDER = r"C:\Users\LENVO\SERVER"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'super_secret_encryption_cookie_key'

USER_DATA = {
    "admin": "m"  # Simplified plain text validation to guarantee no hash mismatch bugs locally
}

@app.template_filter('is_image')
def is_image_filter(filename):
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
    return filename.lower().endswith(image_extensions)

# MIDDLEWARE FIX: Automatically drops the ngrok warning screen for ALL pages/actions
@app.after_request
def add_ngrok_bypass_header(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

@app.route('/')
def index():
    current_user = session.get('user')
    error_msg = session.pop('error', None)
    
    template_path = os.path.join(UPLOAD_FOLDER, 'index.html')
    if not os.path.exists(template_path):
        return "<h1>Error: index.html is missing inside C:\\Users\\LENVO\\SERVER</h1>", 404
        
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f)) and f not in ['index.html', 'app.py']]
    return render_template_string(html_content, current_user=current_user, error_msg=error_msg, files=files)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Clean string matching to guarantee login works instantly
    if username == "admin" and password == "m":
        session['user'] = username
        return redirect('/')
    
    session['error'] = "Invalid credentials. Try again!"
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('user'):
        return "Unauthorized", 401
    if 'file' not in request.files:
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return redirect('/')

@app.route('/files/<filename>')
def download_file(filename):
    if not session.get('user'):
        return "Unauthorized", 401
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
