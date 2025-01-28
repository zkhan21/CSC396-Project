from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from backend.models import expenses_collection

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# 📌 Home Route (For Testing)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to SmartExpense Tracker API!"})

# 📌 Add an Expense (POST)
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    if not all(key in data for key in ("category", "amount", "date", "notes")):
        return jsonify({"error": "Missing required fields"}), 400

    expense = {
        "category": data["category"],
        "amount": data["amount"],
        "date": data["date"],
        "notes": data["notes"]
    }
    expenses_collection.insert_one(expense)
    return jsonify({"message": "Expense added successfully"}), 201

# 📌 Get All Expenses (GET)
@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = list(expenses_collection.find({}, {"_id": 0}))  # Exclude MongoDB IDs
    return jsonify(expenses), 200

if __name__ == '__main__':
    app.run(debug=True)
