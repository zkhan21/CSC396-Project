from flask import Flask, request, jsonify
from backend.models import expenses_collection

app = Flask(__name__)

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