from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.user import User
from datetime import datetime
from database import get_db  # Import the db object
from database import db  # Import the db object
from werkzeug.security import generate_password_hash, check_password_hash
import scrypt  # Import scrypt for password hashing
import os

# Blueprint Setup
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_data = db.users.find_one({'email': email})
        if user_data:
            # Extract the salt and hash from the stored password
            stored_password = user_data['password']
            if stored_password.startswith("scrypt:"):
                _, salt_hex, stored_hash = stored_password.split(":")
                salt = bytes.fromhex(salt_hex)
                
                # Hash the provided password with the stored salt
                hashed_password = scrypt.hash(password.encode('utf-8'), salt, N=16384, r=8, p=1).hex()
                
                # Compare the hashes
                if hashed_password == stored_hash:
                    user = User(user_data)
                    login_user(user)  # Log in the user
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('main.dashboard'))
        
        # If login fails
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        if db.users.find_one({'email': email}):
            flash('An account with this email already exists.', 'error')
            return redirect(url_for('auth.register'))
        else:
            # Generate a random salt
            salt = os.urandom(16)  # 16 bytes (128 bits) of random data
            
            # Hash the password using scrypt
            hashed_password = scrypt.hash(password.encode('utf-8'), salt, N=16384, r=8, p=1).hex()
            
            # Pre-made categories
            pre_made_categories = ['Food', 'Shopping', 'Transport', 'Entertainment', 'Other']
            
            # Insert new user with the hashed password and pre-made categories
            db.users.insert_one({
                'email': email,
                'password': f"scrypt:{salt.hex()}:{hashed_password}",  # Store the salt and hash
                'created_at': datetime.utcnow(),
                'categories': pre_made_categories  # Initialize with pre-made categories
            })
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    flash('You have been logged out. Please log in again to access the dashboard.', 'info')
    return redirect(url_for('auth.login'))