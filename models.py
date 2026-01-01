from db import db
from datetime import datetime
from bson.objectid import ObjectId
from flask_login import UserMixin
import bcrypt

class Person(UserMixin):
    collection = db.persons

    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.name = user_data['name']
        self.age = user_data['age']
        self.email = user_data['email']
        self.password = user_data.get('password', '')
        self.userOrder = user_data.get('userOrder', {})
        self.createdAt = user_data.get('createdAt')

    @staticmethod
    def create(data):
        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user = {
            'name': data['name'],
            'age': data['age'],
            'email': data['email'],
            'password': hashed.decode('utf-8'),
            'userOrder': data.get('userOrder', {}),
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        result = Person.collection.insert_one(user)
        user['_id'] = str(result.inserted_id)
        return Person(user)

    @staticmethod
    def get_all():
        users = list(Person.collection.find())
        for user in users:
            user['_id'] = str(user['_id'])
        return users

    @staticmethod
    def get_by_id(user_id):
        user = Person.collection.find_one({'_id': ObjectId(user_id)})
        if user:
            return Person(user)
        return None

    @staticmethod
    def get_by_email(email):
        user = Person.collection.find_one({'email': email})
        if user:
            return Person(user)
        return None

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def update(user_id, data):
        update_data = {k: v for k, v in data.items() if k in ('name', 'age', 'email', 'userOrder')}
        if 'password' in data:
            update_data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        update_data['updatedAt'] = datetime.utcnow()
        result = Person.collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        return result.matched_count > 0

    @staticmethod
    def delete(user_id):
        result = Person.collection.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0