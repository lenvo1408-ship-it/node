from flask import Flask, request, redirect, render_template_string, send_from_directory, session, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Security secret key needed to handle the logins safely
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key-12345")

# Folder configuration to save uploaded files inside the cloud container
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploaded_files')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Custom filter function for your HTML layout to detect images
@app.template_filter('is_image')
def is_image_filter(filename):
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
    return filename.lower().endswith(image_extensions)

# --- YOUR INSTANT HTML CODE BLOCK ---
MY_HTML_CODE = '''
<!doctype html>
<html>
<head>
    <title>Secure File Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root {
            --text-main: #2d3436;
            --text-muted: #535c68;
            --header-color: #2980b9;
            --box-bg: rgba(244, 244, 249, 0.75);
            --box-border: rgba(255, 255, 255, 0.4);
            --box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            --card-bg: rgba(255, 255, 255, 0.6);
            --card-border: rgba(255, 255, 255, 0.3);
            --thumb-bg: rgba(0, 0, 0, 0.05);
            --footer-bg: rgba(0, 0, 0, 0.03);
            --input-bg: rgba(255, 255, 255, 0.8);
            --input-border: rgba(0, 0, 0, 0.15);
            --btn-gradient: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            --btn-text: #ffffff;
            --link-color: #2980b9;
            --motion-bg: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        }
        [data-theme="dark"] {
            --text-main: #e0e0e6;
            --text-muted: #b3b3b3;
            --header-color: #00f2fe;
            --box-bg: rgba(15, 12, 27, 0.7);
            --box-border: rgba(255, 255, 255, 0.08);
            --box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
            --card-bg: rgba(255, 255, 255, 0.04);
            --card-border: rgba(255, 255, 255, 0.06);
            --thumb-bg: rgba(0, 0, 0, 0.3);
            --footer-bg: rgba(0, 0, 0, 0.2);
            --input-bg: rgba(0, 0, 0, 0.3);
            --input-border: rgba(255, 255, 255, 0.15);
            --btn-gradient: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            --btn-text: #0f0c1b;
            --link-color: #a29bfe;
            --motion-bg: linear-gradient(-45deg, #0f0c1b, #2c1a4d, #124e78, #0a1128);
        }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 30px; min-height: 100vh;
            color: var(--text-main); transition: background 0.3s, color 0.3s;
            background: var(--motion-bg); background-size: 400% 400%; animation: gradientMovement 15s ease infinite;
        }
        @keyframes gradientMovement { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; position: relative; z-index: 10; }
        .theme-toggle-btn {
            background: var(--box-bg); border: 1px solid var(--box-border); color: var(--text-main);
            padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: bold;
            font-size: 14px; display: flex; align-items: center; gap: 8px; box-shadow: var(--box-shadow); backdrop-filter: blur(12px);
        }
        .logout-btn { background: #ff6b6b; color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: bold; font-size: 14px; }
        .logout-btn:hover { background: #ee5a52; }
        h2 { color: var(--header-color); margin-top: 0; font-weight: 600; font-size: 1.4rem; display: flex; align-items: center; gap: 10px; }
        .box { 
            background: var(--box-bg); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); padding: 25px; border-radius: 16px; 
            border: 1px solid var(--box-border); box-shadow: var(--box-shadow); margin-bottom: 25px; position: relative; z-index: 5;
        }
        .file-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 20px; padding: 0; list-style: none; }
        .file-card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; overflow: hidden; text-align: center; display: flex; flex-direction: column; justify-content: space-between; cursor: pointer; transition: all 0.3s ease; }
        .file-card:hover { transform: translateY(-4px); border-color: var(--header-color); }
        .thumbnail-box { width: 100%; height: 130px; background: var(--thumb-bg); display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .thumbnail-box img { width: 100%; height: 100%; object-fit: cover; }
        .file-icon { font-size: 45px; }
        .file-info { padding: 12px; font-size: 13px; word-break: break-all; background: var(--footer-bg); border-top: 1px solid var(--card-border); flex-grow: 1; display: flex; align-items: center; justify-content: center; }
        a { color: var(--link-color); text-decoration: none; font-weight: bold; }
        input[type=text], input[type=password] { background: var(--input-bg); color: var(--text-main); border: 1px solid var(--input-border); padding: 10px; border-radius: 8px; width: 100%; box-sizing: border-box; margin-bottom: 12px; }
        input[type=file] { color: var(--text-muted); background: var(--input-bg); padding: 10px; border-radius: 8px; border: 1px dashed var(--input-border); width: 100%; box-sizing: border-box; margin-bottom: 12px; }
        input[type=submit], .login-btn { background: var(--btn-gradient); color: var(--btn-text); border: 0; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: all 0.3s ease; }
        input[type=submit]:hover, .login-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.2); }
    </style>
</head>
<body>

    <div class="top-bar">
        {% if current_user %}
            <div style="color: var(--text-main); font-weight: bold;">👤 {{ current_user }}</div>
            <div style="display: flex; gap: 10px;">
                <button class="theme-toggle-btn" id="themeToggle">
                    <span id="themeIcon">🌙</span> <span id="themeText">Dark Mode</span>
                </button>
                <form method="post" action="/logout" style="margin: 0;">
                    <button type="submit" class="logout-btn">Logout</button>
                </form>
            </div>
        {% else %}
            <button class="theme-toggle-btn" id="themeToggle">
                <span id="themeIcon">🌙</span> <span id="themeText">Dark Mode</span>
            </button>
        {% endif %}
    </div>

    {% if current_user %}
    <div class="box">
        <h2>📤 Cloud Upload</h2>
        <form method="post" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="UPLOAD TO SERVER">
        </form>
    </div>
    
    <div class="box">
        <h2>📁 Storage Gallery</h2>
        <ul class="file-grid">
        {% for filename in files %}
            <li class="file-card">
                <a href="/files/{{ filename }}" target="_blank">
                    <div class="thumbnail-box">
                        {% if filename | is_image %}
                            <img src="/files/{{ filename }}" alt="thumb">
                        {% else %}
                            <div class="file-icon">📄</div>
                        {% endif %}
                    </div>
                </a>
                <div class="file-info">
                    <a href="/files/{{ filename }}" target="_blank">{{ filename }}</a>
                </div>
            </li>
        {% else %}
            <li style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 20px;">No files stored on the server yet.</li>
        {% endfor %}
        </ul>
    </div>
    {% else %}
    <div class="box" style="max-width: 400px; margin: 100px auto;">
        <h2>🔐 Authorization Required</h2>
        {% if error_msg %}<p style="color: #ff7675; font-size: 14px; font-weight: bold;">{{ error_msg }}</p>{% endif %}
        <form method="post" action="/login">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="LOGIN" class="login-btn">
        </form>
    </div>
    {% endif %}

    <script>
        const toggleBtn = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const themeText = document.getElementById('themeText');
        const currentTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', currentTheme);
        updateToggleUI(currentTheme);

        toggleBtn.addEventListener('click', () => {
            let targetTheme = 'light';
            if (document.documentElement.getAttribute('data-theme') === 'light') { targetTheme = 'dark'; }
            document.documentElement.setAttribute('data-theme', targetTheme);
            localStorage.setItem('theme', targetTheme);
            updateToggleUI(targetTheme);
        });

        function updateToggleUI(theme) {
            if (theme === 'dark') { themeIcon.textContent = '☀️'; themeText.textContent = 'Light Mode'; } 
            else { themeIcon.textContent = '🌙'; themeText.textContent = 'Dark Mode'; }
        }
    </script>
</body>
</html>
'''
# --- END OF HTML ---

@app.route('/')
def index():
    current_user = session.get('user')
    files = []
    if current_user and os.path.exists(app.config['UPLOAD_FOLDER']):
        files = os.listdir(app.config['UPLOAD_FOLDER'])
    error_msg = request.args.get('error_msg')
    return render_template_string(MY_HTML_CODE, current_user=current_user, files=files, error_msg=error_msg)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simple default credentials - change these if you want!
    if username == "admin" and password == "password123":
        session['user'] = username
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index', error_msg="Invalid credentials!"))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user' not in session:
        return redirect(url_for('index'))
    if 'file' not in request.files:
        return redirect(url_for('index', error_msg="No file provided"))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index', error_msg="No file selected"))
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    
    return redirect(url_for('index', error_msg="Upload failed"))

@app.route('/files/<filename>')
def serve_file(filename):
    if 'user' not in session:
        return redirect(url_for('index'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], secure_filename(filename))

if __name__ == '__main__':
    app.run(debug=True)
