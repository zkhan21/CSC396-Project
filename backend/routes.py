import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend.models import expenses_collection

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Corrected version

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, '../templates'))

CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

@app.before_request
def log_request_info():
    print("\n🚀 Incoming Request 🚀")
    print(f"➡️ Method: {request.method}")
    print(f"➡️ Path: {request.path}")
    print(f"➡️ Headers: {dict(request.headers)}")
    print(f"➡️ Body: {request.get_data()}\n")


@app.route('/')
def home():
    return render_template('index.html')


# 📌 Add Expense (POST)
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

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


@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = list(expenses_collection.find({}, {"_id": 0}))  # Exclude MongoDB IDs
    return jsonify(expenses), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

