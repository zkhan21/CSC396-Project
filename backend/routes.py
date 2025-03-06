from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from backend.models import expenses_collection, users_collection
from jinja2 import FileSystemLoader
import bcrypt
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # This should be backend/
TEMPLATE_DIR = os.path.join(BASE_DIR, '../templates')  # Go up one level to find templates
STATIC_DIR = os.path.join(BASE_DIR, '../static')  # Adjust for static files

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
app.jinja_loader = FileSystemLoader(TEMPLATE_DIR)
CORS(app)
app.secret_key = "supersecretkey"  # 🔒 TODO: Move this to environment variables in production

# Ensure the session is maintained correctly
@app.before_request
def ensure_session():
    """ Ensures session consistency across requests """
    session.permanent = True  # Makes session persist longer
    if 'user' not in session:
        return  # Prevents clearing session data unnecessarily

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handles user login """
    error = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password', '').encode('utf-8')

        user = users_collection.find_one({"email": email})

        if user:
            stored_password = user["password"].encode('utf-8')

            try:
                if bcrypt.checkpw(password, stored_password):
                    session['user'] = email
                    flash("Login successful!", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash("Incorrect email or password.", "error")
            except Exception as e:
                flash("An error occurred during login. Please try again.", "error")
        else:
            flash("Incorrect email or password.", "error")

    return render_template('login.html', error=error)

def hash_password(password):
    """ Hash a given password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Handles user registration """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if users_collection.find_one({"email": email}):
            flash("User already exists! Try logging in.", "error")
            return redirect(url_for('register'))

        hashed_password = hash_password(password)

        users_collection.insert_one({
            "email": email,
            "password": hashed_password.decode('utf-8')
        })

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """ Ensures only logged-in users can access the dashboard """
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    
    flash("You need to log in to access the dashboard.", "error")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """ Handles user logout """
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.context_processor
def inject_session():
    """ Injects session data into all templates """
    return dict(session=session)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
