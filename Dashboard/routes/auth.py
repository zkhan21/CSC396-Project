# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user  # Add this import
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from models.user import User
from datetime import datetime  # Add this import for registration

load_dotenv()

# MongoDB Connection
client = MongoClient(os.environ.get('MONGO_URI'))
db = client.get_database()

# Blueprint Setup
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_data = db.users.find_one({'email': email})
        if user_data and user_data['password'] == password:  # Plain-text comparison for testing
            user = User(user_data)
            login_user(user)  # Log in the user
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        if db.users.find_one({'email': email}):
            flash('Email already registered')
        else:
            # Insert new user
            db.users.insert_one({
                'email': email,
                'password': password,  # Plain-text password for testing
                'created_at': datetime.utcnow()
            })
            flash('Registration successful! Please log in.')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')