from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from backend.models import expenses_collection, users_collection, categories_collection
from jinja2 import FileSystemLoader
import bcrypt
import os

# Setup Flask App
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # This should be backend/
TEMPLATE_DIR = os.path.join(BASE_DIR, '../templates')  # Go up one level to find templates
STATIC_DIR = os.path.join(BASE_DIR, '../static')  # Adjust for static files

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
app.jinja_loader = FileSystemLoader(TEMPLATE_DIR)
CORS(app)
app.secret_key = "supersecretkey"  # 🔒 TODO: Move this to environment variables in production

# Ensure session is persistent
@app.before_request
def ensure_session():
    """ Ensures session consistency across requests """
    session.permanent = True
    if 'user' not in session:
        return  # Prevents clearing session data unnecessarily

# Home Route
@app.route('/')
def home():
    html = render_template('index.html')
    print("🔍 Flask is sending this HTML to the browser:\n", html)  # Print to console
    return html


# Login Route
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
                    return redirect(url_for('new_dashboard'))  # Redirect to the new dashboard
                else:
                    flash("Incorrect email or password.", "error")
            except Exception as e:
                flash("An error occurred during login. Please try again.", "error")
        else:
            flash("Incorrect email or password.", "error")

    return render_template('login.html', error=error)

# Hash Password Function
def hash_password(password):
    """ Hash a given password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Register Route
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

# Old Dashboard Route (kept for reference)
@app.route('/dashboard')
def dashboard():
    """ Legacy Dashboard Route """
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    
    flash("You need to log in to access the dashboard.", "error")
    return redirect(url_for('login'))

# **NEW DASHBOARD ROUTE**
@app.route('/new_dashboard')
def new_dashboard():
    """ New Dashboard Route """
    if 'user' in session:
        user_email = session['user']
        return render_template('new_dashboard.html', user=user_email)
    
    flash("You need to log in to access the dashboard.", "error")
    return redirect(url_for('login'))

# Add Category Route
@app.route('/add_category', methods=['POST'])
def add_category():
    """ Allows users to add a new category """
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.json
    category_name = data.get("category")

    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    categories_collection.insert_one({
        "user": session['user'],
        "category": category_name
    })

    return jsonify({"message": "Category added successfully"}), 201

# Get Categories Route
@app.route('/get_categories', methods=['GET'])
def get_categories():
    """ Fetch categories for the logged-in user """
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    categories = list(categories_collection.find({"user": session['user']}, {"_id": 0, "category": 1}))
    return jsonify(categories)

# Logout Route
@app.route('/logout')
def logout():
    """ Handles user logout """
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# Inject session data into templates
@app.context_processor
def inject_session():
    """ Injects session data into all templates """
    return dict(session=session)

# Run Flask App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
