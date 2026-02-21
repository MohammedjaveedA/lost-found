from bson import ObjectId
from datetime import datetime
from extensions import mongo

class Organization:
    @staticmethod
    def get_collection():
        return mongo.db.organizations
    
    @staticmethod
    def create_organization(name, address, created_by):
        """Create a new organization listing"""
        collection = Organization.get_collection()
        org_data = {
            'name': name,
            'address': address,
            'created_by': ObjectId(created_by),
            'created_at': datetime.utcnow()
        }
        result = collection.insert_one(org_data)
        org_data['_id'] = result.inserted_id
        return org_data
    
    @staticmethod
    def get_all_organizations():
        """Get all organizations for dropdown"""
        collection = Organization.get_collection()
        return list(collection.find())
    
    @staticmethod
    def get_organization_by_id(org_id):
        """Get organization by ID"""
        collection = Organization.get_collection()
        return collection.find_one({'_id': ObjectId(org_id)})
    
    @staticmethod
    def get_organization_by_admin(admin_id):
        """Get organization created by specific admin"""
        collection = Organization.get_collection()
        return collection.find_one({'created_by': ObjectId(admin_id)})
    
    @staticmethod
    def update_organization(org_id, name, address):
        """Update organization details"""
        collection = Organization.get_collection()
        return collection.update_one(
            {'_id': ObjectId(org_id)},
            {'$set': {
                'name': name,
                'address': address,
                'updated_at': datetime.utcnow()
            }}
        )