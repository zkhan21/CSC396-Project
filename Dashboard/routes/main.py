from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.transaction import Transaction
from database import db
from bson.objectid import ObjectId
from datetime import datetime

main_bp = Blueprint('main', __name__)

# Home Route (unchanged)
@main_bp.route('/')
def home():
    current_date = datetime.now().strftime('%B %d, %Y')  # March 16, 2025
    current_time = datetime.now().strftime('%I:%M %p')   # 6:44 AM
    return render_template('home.html', current_date=current_date, current_time=current_time)

# Dashboard Route (new route for authenticated users)
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Transactions Route (unchanged)
@main_bp.route('/transactions')
@login_required
def transactions():
    # Get transactions for the current user
    transactions = list(Transaction.get_by_user_id(db, current_user.id))
    
    # Calculate summary data for charts
    summary = {
        'total': sum(t['amount'] for t in transactions),
        'categories': [],  # List of categories
        'amounts': [],    # List of amounts corresponding to categories
        'dates': [],      # List of unique dates
        'trend_amounts': []  # List of total amounts per date
    }

    # Calculate spending by category
    by_category = {}
    for t in transactions:
        by_category[t['category']] = by_category.get(t['category'], 0) + t['amount']
    
    # Populate categories and amounts for the pie chart
    summary['categories'] = list(by_category.keys())
    summary['amounts'] = list(by_category.values())

    # Calculate spending trend over time (by date)
    by_date = {}
    for t in transactions:
        date_str = t['date'].strftime('%Y-%m-%d')  # Format date as string
        by_date[date_str] = by_date.get(date_str, 0) + t['amount']
    
    # Populate dates and trend_amounts for the line chart
    summary['dates'] = list(by_date.keys())
    summary['trend_amounts'] = list(by_date.values())

    return render_template('transactions.html', transactions=transactions, summary=summary)

# Categories Route (unchanged)
@main_bp.route('/categories')
@login_required
def categories():
    pre_made_categories = ['Food', 'Shopping', 'Transport', 'Entertainment', 'Other']
    
    # Fetch user-specific categories from the database
    user = db.users.find_one({'_id': ObjectId(current_user.id)})
    user_categories = user.get('categories', [])  # Get the user's custom categories
    
    return render_template('categories.html', pre_made_categories=pre_made_categories, user_categories=user_categories)

# Add Category Route (unchanged)
@main_bp.route('/add_category', methods=['POST'])
@login_required
def add_category():
    category_name = request.form.get('category_name')
    if category_name:
        # Add the category to the user's list in the database
        db.users.update_one(
            {'_id': ObjectId(current_user.id)},
            {'$addToSet': {'categories': category_name}}
        )
        flash(f'Category "{category_name}" added successfully!', 'success')
    return redirect(url_for('main.categories'))

# Delete Category Route (unchanged)
@main_bp.route('/delete_category', methods=['POST'])
@login_required
def delete_category():
    category_name = request.form.get('category_name')
    if category_name:
        # Remove the category from the user's list in the database
        db.users.update_one(
            {'_id': ObjectId(current_user.id)},
            {'$pull': {'categories': category_name}}
        )
        flash(f'Category "{category_name}" deleted successfully!', 'success')
    return redirect(url_for('main.categories'))

# Add Transaction Route (unchanged)
@main_bp.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    # Pre-defined categories
    pre_made_categories = ['Food', 'Shopping', 'Transport', 'Entertainment', 'Other']
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.today().strftime('%Y-%m-%d')
    
    # Fetch user-specific categories from the database
    user = db.users.find_one({'_id': ObjectId(current_user.id)})
    user_categories = user.get('categories', [])  # Get the user's custom categories
    
    if request.method == 'POST':
        # Handle form submission
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        description = request.form.get('description')
        date = request.form.get('date')  # Get the date from the form
        
        # Create and save the transaction
        transaction = Transaction(current_user.id, amount, category, description, date)
        transaction.save(db)
        
        flash('Transaction added successfully!')
        return redirect(url_for('main.transactions'))
    
    # Render the form with today's date, pre-made categories, and user categories
    return render_template('add_transaction.html', today=today, pre_made_categories=pre_made_categories, user_categories=user_categories)

# Delete Transaction Route (unchanged)
@main_bp.route('/delete_transaction/<transaction_id>')
@login_required
def delete_transaction(transaction_id):
    Transaction.delete_by_id(db, transaction_id)
    flash('Transaction deleted successfully!')
    return redirect(url_for('main.transactions'))

# Edit Transaction Route (unchanged)
@main_bp.route('/edit_transaction/<transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Handle form submission
        update_data = {
            'amount': float(request.form.get('amount')),
            'category': request.form.get('category'),
            'description': request.form.get('description'),
            'date': request.form.get('date')  # Update the date from the form
        }
        Transaction.update_by_id(db, transaction_id, update_data)
        
        flash('Transaction updated successfully!')
        return redirect(url_for('main.transactions'))
    
    # Fetch the transaction to edit
    transaction = db.transactions.find_one({'_id': ObjectId(transaction_id)})
    
    # Render the edit form with the transaction data
    return render_template('edit_transaction.html', transaction=transaction)

# Bulk Delete Transactions Route (unchanged)
@main_bp.route('/delete_transactions', methods=['POST'])
@login_required
def delete_transactions():
    transaction_ids = request.form.getlist('transaction_ids')
    if transaction_ids:
        transaction_ids = [ObjectId(tid) for tid in transaction_ids]
        db.transactions.delete_many({'_id': {'$in': transaction_ids}})
        flash(f'{len(transaction_ids)} transactions deleted successfully!', 'success')
    else:
        flash('No transactions selected.', 'error')
    return redirect(url_for('main.transactions'))