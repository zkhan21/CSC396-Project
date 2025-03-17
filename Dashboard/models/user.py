from flask_login import UserMixin
from bson import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])  # Convert ObjectId to string
        self.first_name = user_data.get('first_name', '')  # Retrieve first name
        self.last_name = user_data.get('last_name', '')  # Retrieve last name
        self.email = user_data['email']
        self.password = user_data['password']

    @staticmethod
    def get_by_id(db, user_id):
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_email(db, email):
        user_data = db.users.find_one({'email': email})
        return User(user_data) if user_data else None