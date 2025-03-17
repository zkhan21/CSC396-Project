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
    filter_date = request.args.get('filter_date')
    filter_category = request.args.get('filter_category')

    # Get transactions for the current user
    query = {'user_id': current_user.id}

    if filter_date:
        query['date'] = datetime.strptime(filter_date, '%Y-%m-%d')
    
    if filter_category:
        query['category'] = filter_category

    transactions = list(Transaction.get_filtered(db, query))

    # Calculate summary data for charts
    summary = {
        'total': sum(t['amount'] for t in transactions),
        'categories': list(set(t['category'] for t in transactions)),  # Unique categories
        'amounts': [],
        'dates': [],
        'trend_amounts': []
    }

    # Calculate spending trend and categories
    by_category = {}
    by_date = {}

    for t in transactions:
        by_category[t['category']] = by_category.get(t['category'], 0) + t['amount']
        
        date_str = t['date'].strftime('%Y-%m-%d')
        by_date[date_str] = by_date.get(date_str, 0) + t['amount']

    summary['amounts'] = list(by_category.values())
    summary['dates'] = list(by_date.keys())
    summary['trend_amounts'] = list(by_date.values())

    return render_template('transactions.html', transactions=transactions, summary=summary)


# Categories Route (unchanged)
@main_bp.route('/categories')
@login_required
def categories():
    # Fetch user-specific categories from the database
    user = db.users.find_one({'_id': ObjectId(current_user.id)})
    user_categories = user.get('categories', [])  # Get the user's custom categories
    
    return render_template('categories.html', user_categories=user_categories)


# Add Category Route (updated)
@main_bp.route('/add_category', methods=['POST'])
@login_required
def add_category():
    category_name = request.form.get('category_name')
    if category_name:
        # Fetch user-specific categories from the database
        user = db.users.find_one({'_id': ObjectId(current_user.id)})
        user_categories = user.get('categories', [])  # Get the user's custom categories
        
        # Check if the category already exists
        if category_name in user_categories:
            flash(f'Category "{category_name}" already exists!', 'error')
        else:
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
        date_str = request.form.get('date')  # Get the date from the form as a string
        
        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Create and save the transaction
        transaction = Transaction(current_user.id, amount, category, description, date)
        transaction.save(db)
        
        flash('Transaction added successfully!')
        return redirect(url_for('main.transactions'))
    
    # Render the form with today's date and user categories
    return render_template('add_transaction.html', today=today, user_categories=user_categories)

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
    # Fetch the transaction to edit
    transaction = db.transactions.find_one({'_id': ObjectId(transaction_id)})
    
    # Fetch user-specific categories from the database
    user = db.users.find_one({'_id': ObjectId(current_user.id)})
    user_categories = user.get('categories', [])  # Get the user's custom categories
    
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
    
    # Render the edit form with the transaction data and user categories
    return render_template('edit_transaction.html', transaction=transaction, user_categories=user_categories)

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