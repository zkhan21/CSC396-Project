from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.transaction import Transaction
from database import db  # ✅ Import db from database.py
from bson.objectid import ObjectId  # ✅ Import ObjectId

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    # Get transactions for the current user
    transactions = list(Transaction.get_by_user_id(db, current_user.id))
    
    # Calculate summary data for charts
    summary = {
        'total': sum(t['amount'] for t in transactions),
        'by_category': {}
    }
    for t in transactions:
        summary['by_category'][t['category']] = summary['by_category'].get(t['category'], 0) + t['amount']
    
    return render_template('dashboard.html', transactions=transactions, summary=summary)

@main_bp.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        description = request.form.get('description')
        
        transaction = Transaction(current_user.id, amount, category, description)
        transaction.save(db)  # ✅ db is now properly defined
        flash('Transaction added successfully!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_transaction.html')

@main_bp.route('/delete_transaction/<transaction_id>')
@login_required
def delete_transaction(transaction_id):
    Transaction.delete_by_id(db, transaction_id)  # ✅ db is now properly defined
    flash('Transaction deleted successfully!')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/edit_transaction/<transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    if request.method == 'POST':
        update_data = {
            'amount': float(request.form.get('amount')),
            'category': request.form.get('category'),
            'description': request.form.get('description')
        }
        Transaction.update_by_id(db, transaction_id, update_data)  # ✅ db is now properly defined
        flash('Transaction updated successfully!')
        return redirect(url_for('main.dashboard'))
    
    transaction = db.users.find_one({'_id': ObjectId(transaction_id)})  # ✅ Fix db reference
    return render_template('edit_transaction.html', transaction=transaction)
