from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample route
@app.route('/')
def home():
    return "Welcome to SmartExpense Tracker API!"

if __name__ == '__main__':
    app.run(debug=True)
