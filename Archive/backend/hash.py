from backend.models import users_collection
import bcrypt

# Fetch all users
users = users_collection.find()

for user in users:
    stored_password = user["password"]

    # Only hash if password is still plaintext
    if not stored_password.startswith("$2b$"):
        hashed_password = bcrypt.hashpw(stored_password.encode('utf-8'), bcrypt.gensalt())
        users_collection.update_one({"_id": user["_id"]}, {"$set": {"password": hashed_password.decode('utf-8')}})

print("✅ All passwords have been securely hashed in the database!")
