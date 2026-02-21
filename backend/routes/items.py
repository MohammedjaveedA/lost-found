from flask import Blueprint, request, jsonify
from models.item import Item
from models.user import User
from middleware.auth import jwt_required
from bson import ObjectId

items_bp = Blueprint('items', __name__)

@items_bp.route('/', methods=['GET'])
@jwt_required
def get_items():
    """Get items for user's organization"""
    current_user = request.current_user
    
    # Regular users must have organization
    if current_user['role'] == 'regular' and not current_user.get('organization_id'):
        return jsonify({'error': 'Please select an organization first'}), 400
    
    # Get query params
    status = request.args.get('status')
    item_type = request.args.get('type', 'all')
    
    # Get items
    items = Item.get_items_by_organization(
        str(current_user['organization_id']),
        status,
        item_type
    )
    
    # Get user details for each item
    result = []
    for item in items:
        user = User.find_by_id(item['user_id'])
        result.append({
            'id': str(item['_id']),
            'type': item['type'],
            'title': item['title'],
            'description': item['description'],
            'category': item['category'],
            'location': item['location'],
            'date': item['date'],
            'phone_number': item.get('phone_number', ''),
            'status': item['status'],
            'created_at': item['created_at'],
            'user': {
                'id': str(user['_id']),
                'name': user['name']
            }
        })
    
    return jsonify({'items': result}), 200

@items_bp.route('/', methods=['POST'])
@jwt_required
def create_item():
    """Create a new lost/found item"""
    current_user = request.current_user
    data = request.get_json()
    
    # Regular users must have organization
    if current_user['role'] == 'regular' and not current_user.get('organization_id'):
        return jsonify({'error': 'Please select an organization first'}), 400
    
    # Validate required fields
    required = ['type', 'title', 'description', 'category', 'location', 'date']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate item type
    if data['type'] not in ['lost', 'found']:
        return jsonify({'error': 'Type must be "lost" or "found"'}), 400
    
    # Create item
    item = Item.create_item(
        user_id=str(current_user['_id']),
        organization_id=str(current_user['organization_id']),
        item_type=data['type'],
        title=data['title'],
        description=data['description'],
        category=data['category'],
        location=data['location'],
        date=data['date'],
        phone_number=data['phone_number']
    )
    
    return jsonify({
        'message': 'Item posted successfully',
        'item': {
            'id': str(item['_id']),
            'type': item['type'],
            'title': item['title'],
            'status': item['status']
        }
    }), 201

@items_bp.route('/my', methods=['GET'])
@jwt_required
def get_my_items():
    """Get items posted by current user"""
    current_user = request.current_user
    
    items = Item.get_user_items(str(current_user['_id']))
    
    result = []
    for item in items:
        result.append({
            'id': str(item['_id']),
            'type': item['type'],
            'title': item['title'],
            'description': item['description'],
            'category': item['category'],
            'location': item['location'],
            'date': item['date'],
            'phone_number': item.get('phone_number', ''),  
            'status': item['status'],
            'created_at': item['created_at']
        })
    
    return jsonify({'items': result}), 200

@items_bp.route('/<item_id>', methods=['GET'])
@jwt_required
def get_item(item_id):
    """Get single item details"""
    current_user = request.current_user
    
    item = Item.get_item_by_id(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    # Check if item belongs to user's organization
    if str(item['organization_id']) != str(current_user['organization_id']):
        return jsonify({'error': 'Access denied'}), 403
    
    user = User.find_by_id(item['user_id'])
    
    return jsonify({
        'item': {
            'id': str(item['_id']),
            'type': item['type'],
            'title': item['title'],
            'description': item['description'],
            'category': item['category'],
            'location': item['location'],
            'date': item['date'],
            'status': item['status'],
            'created_at': item['created_at'],
            'user': {
                'id': str(user['_id']),
                'name': user['name']
            }
        }
    }), 200

@items_bp.route('/<item_id>', methods=['PUT'])
@jwt_required
def update_item(item_id):
    """Update item (only by owner)"""
    current_user = request.current_user
    data = request.get_json()
    
    # Only allow updating specific fields
    allowed_fields = ['title', 'description', 'category', 'location', 'date']
    update_data = {k: v for k, v in data.items() if k in allowed_fields}
    
    result = Item.update_item(item_id, str(current_user['_id']), update_data)
    
    if result.modified_count == 0:
        return jsonify({'error': 'Item not found or unauthorized'}), 404
    
    return jsonify({'message': 'Item updated successfully'}), 200

@items_bp.route('/<item_id>/resolve', methods=['PUT'])
@jwt_required
def resolve_item(item_id):
    """Mark item as resolved"""
    current_user = request.current_user
    
    result = Item.mark_resolved(item_id, str(current_user['_id']))
    
    if result.modified_count == 0:
        return jsonify({'error': 'Item not found or unauthorized'}), 404
    
    return jsonify({'message': 'Item marked as resolved'}), 200

@items_bp.route('/<item_id>', methods=['DELETE'])
@jwt_required
def delete_item(item_id):
    """Delete item (only by owner)"""
    current_user = request.current_user
    
    result = Item.delete_item(item_id, str(current_user['_id']))
    
    if result.deleted_count == 0:
        return jsonify({'error': 'Item not found or unauthorized'}), 404
    
    return jsonify({'message': 'Item deleted successfully'}), 200