from flask import Flask, render_template, request, redirect, url_for, jsonify, session
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
app.secret_key = "supersecretkey"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        user = users_collection.find_one({"email": email})

        if user:
            stored_password = user["password"].encode('utf-8')  # Convert back to bytes

            # Check hashed password
            if bcrypt.checkpw(password, stored_password):
                session['user'] = email
                return redirect(url_for('dashboard'))
            else:
                error = "Incorrect email or password."
        else:
            error = "Incorrect email or password."

    return render_template('login.html', error=error)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        if users_collection.find_one({"email": email}):
            return "User already exists!"

        # Hash the password
        hashed_password = hash_password(password)

        # Store user with hashed password
        users_collection.insert_one({
            "email": email,
            "password": hashed_password.decode('utf-8')  # Store as string
        })

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear session
    return redirect(url_for('login'))  # Redirect to login

@app.context_processor
def inject_session():
    return dict(session=session)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
