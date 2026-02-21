from flask import Blueprint, request, jsonify
from models.organization import Organization
from middleware.auth import jwt_required, org_admin_required
from bson import ObjectId

org_bp = Blueprint('organizations', __name__)

@org_bp.route('/', methods=['GET'])
def get_organizations():
    """Get all organizations (for user dropdown)"""
    organizations = Organization.get_all_organizations()
    
    result = []
    for org in organizations:
        result.append({
            'id': str(org['_id']),
            'name': org['name'],
            'address': org.get('address', '')
        })
    
    return jsonify({'organizations': result}), 200

@org_bp.route('/my', methods=['GET'])
@org_admin_required
def get_my_organization():
    """Get organization details for logged-in admin"""
    current_user = request.current_user
    
    org = Organization.get_organization_by_admin(str(current_user['_id']))
    
    if not org:
        return jsonify({'error': 'Organization not found'}), 404
    
    return jsonify({
        'organization': {
            'id': str(org['_id']),
            'name': org['name'],
            'address': org.get('address', ''),
            'created_at': org.get('created_at')
        }
    }), 200

@org_bp.route('/<org_id>', methods=['GET'])
def get_organization(org_id):
    """Get specific organization details"""
    org = Organization.get_organization_by_id(org_id)
    
    if not org:
        return jsonify({'error': 'Organization not found'}), 404
    
    return jsonify({
        'organization': {
            'id': str(org['_id']),
            'name': org['name'],
            'address': org.get('address', '')
        }
    }), 200

@org_bp.route('/<org_id>', methods=['PUT'])
@org_admin_required
def update_organization(org_id):
    """Update organization (only by its admin)"""
    current_user = request.current_user
    data = request.get_json()
    
    # Verify this org belongs to the admin
    org = Organization.get_organization_by_admin(str(current_user['_id']))
    
    if not org or str(org['_id']) != org_id:
        return jsonify({'error': 'Unauthorized to edit this organization'}), 403
    
    # Update fields
    name = data.get('name', org['name'])
    address = data.get('address', org.get('address', ''))
    
    Organization.update_organization(org_id, name, address)
    
    return jsonify({'message': 'Organization updated successfully'}), 200