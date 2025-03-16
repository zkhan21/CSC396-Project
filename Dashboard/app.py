from flask import Flask
from flask_login import LoginManager
from database import db  # ✅ Import db from database.py
from models.user import User
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(db, user_id)

# Test route to verify MongoDB connection and query users
@app.route('/test_db')
def test_db():
    try:
        # Test database connection
        db.command('ping')
        print("Database ping successful!")

        # Query the users collection
        users = db.users.find()
        user_count = db.users.count_documents({})
        print(f"Found {user_count} users in the database.")

        # Print user details
        for user in users:
            print(f"User: {user}")

        return f"Database connection successful! Found {user_count} users.", 200
    except Exception as e:
        return f"Database connection or query failed: {e}", 500

# Import and Register Blueprints
from routes.auth import auth_bp
from routes.main import main_bp
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)