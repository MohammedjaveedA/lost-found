from bson import ObjectId
from datetime import datetime
from extensions import mongo

class Item:
    @staticmethod
    def get_collection():
        return mongo.db.items
    
    @staticmethod
    def create_item(user_id, organization_id, item_type, title, description, 
                   category, location, date,phone_number):
        """Create a lost/found item post"""
        collection = Item.get_collection()
        item_data = {
            'user_id': ObjectId(user_id),
            'organization_id': ObjectId(organization_id),
            'type': item_type,  # 'lost' or 'found'
            'title': title,
            'description': description,
            'category': category,
            'location': location,
            'date': date,
            'phone_number': phone_number, 
            'status': 'open',  # 'open' or 'resolved'
            'created_at': datetime.utcnow()
        }
        result = collection.insert_one(item_data)
        item_data['_id'] = result.inserted_id
        return item_data
    
    @staticmethod
    def get_items_by_organization(org_id, status=None, item_type=None):
        """Get all items for an organization with optional filters"""
        collection = Item.get_collection()
        query = {'organization_id': ObjectId(org_id)}
        
        if status:
            query['status'] = status
        if item_type and item_type != 'all':
            query['type'] = item_type
            
        return list(collection.find(query).sort('created_at', -1))
    
    @staticmethod
    def get_user_items(user_id):
        """Get items posted by a specific user"""
        collection = Item.get_collection()
        return list(collection.find(
            {'user_id': ObjectId(user_id)}
        ).sort('created_at', -1))
    
    @staticmethod
    def get_item_by_id(item_id):
        """Get single item by ID"""
        collection = Item.get_collection()
        return collection.find_one({'_id': ObjectId(item_id)})
    
    @staticmethod
    def update_item(item_id, user_id, update_data):
        """Update item (only if user owns it)"""
        collection = Item.get_collection()
        return collection.update_one(
            {
                '_id': ObjectId(item_id),
                'user_id': ObjectId(user_id)
            },
            {'$set': update_data}
        )
    
    @staticmethod
    def mark_resolved(item_id, user_id):
        """Mark item as resolved"""
        collection = Item.get_collection()
        return collection.update_one(
            {
                '_id': ObjectId(item_id),
                'user_id': ObjectId(user_id)
            },
            {'$set': {'status': 'resolved'}}
        )
    
    @staticmethod
    def delete_item(item_id, user_id):
        """Delete item (only if user owns it)"""
        collection = Item.get_collection()
        return collection.delete_one({
            '_id': ObjectId(item_id),
            'user_id': ObjectId(user_id)
        })