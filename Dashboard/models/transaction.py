# models/transaction.py
from datetime import datetime
from bson import ObjectId

class Transaction:
    def __init__(self, user_id, amount, category, description, date=None):
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date or datetime.utcnow()

    def save(self, db):
        return db.transactions.insert_one({
            'user_id': self.user_id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date
        })

    @staticmethod
    def get_by_user_id(db, user_id):
        return list(db.transactions.find({'user_id': user_id}))

    @staticmethod
    def delete_by_id(db, transaction_id):
        return db.transactions.delete_one({'_id': ObjectId(transaction_id)})

    @staticmethod
    def update_by_id(db, transaction_id, update_data):
        return db.transactions.update_one(
            {'_id': ObjectId(transaction_id)},
            {'$set': update_data}
        )
    @staticmethod
    def get_filtered(db, query):
        return db.transactions.find(query)
