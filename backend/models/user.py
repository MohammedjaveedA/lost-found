from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime
from extensions import mongo  # Import mongo from extensions

class User:
    @staticmethod
    def get_collection():
        return mongo.db.users
    
    @staticmethod
    def create_user(name, email, password, role, organization_id=None):
        """Create a new user"""
        collection = User.get_collection()
        user_data = {
            'name': name,
            'email': email.lower(),
            'password': generate_password_hash(password),
            'role': role,  # 'org_admin' or 'regular'
            'organization_id': ObjectId(organization_id) if organization_id else None,
            'created_at': datetime.utcnow()
        }
        result = collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        collection = User.get_collection()
        return collection.find_one({'email': email.lower()})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        collection = User.get_collection()
        return collection.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def verify_password(user, password):
        """Verify password"""
        return check_password_hash(user['password'], password)
    
    @staticmethod
    def update_organization(user_id, org_id):
        """Update user's organization (for regular users)"""
        collection = User.get_collection()
        return collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'organization_id': ObjectId(org_id)}}
        )