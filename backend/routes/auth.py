from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from models.organization import Organization
from bson import ObjectId
from datetime import datetime
import re
from middleware.auth import jwt_required  # Add this import

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register/org', methods=['POST'])
def register_org():
    """Register as organization admin"""
    data = request.get_json()
    
    # Validate input
    if not all(k in data for k in ['name', 'email', 'password', 'org_name', 'org_address']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.find_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user as org_admin
    user = User.create_user(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role='org_admin'
    )
    
    # Create organization
    org = Organization.create_organization(
        name=data['org_name'],
        address=data['org_address'],
        created_by=str(user['_id'])
    )
    
    # Update user with organization_id
    User.update_organization(str(user['_id']), str(org['_id']))
    
    # Generate token
    access_token = create_access_token(identity=str(user['_id']))
    
    return jsonify({
        'message': 'Organization registered successfully',
        'token': access_token,
        'user': {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'organization': {
                'id': str(org['_id']),
                'name': org['name']
            }
        }
    }), 201
@auth_bp.route('/register/user', methods=['POST'])
def register_user():
    """Register as regular user (student/staff) with organization"""
    data = request.get_json()
    
    # Validate input
    required_fields = ['name', 'email', 'password', 'organization_id']
    if not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields. Organization selection is mandatory'}), 400
    
    # Check if user exists
    if User.find_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 409
    
    # Verify organization exists
    org = Organization.get_organization_by_id(data['organization_id'])
    if not org:
        return jsonify({'error': 'Selected organization not found'}), 404
    
    # Create user with organization
    user = User.create_user(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role='regular',
        organization_id=data['organization_id']  # Pass organization_id
    )
    
    # Get organization details for response
    org_data = Organization.get_organization_by_id(data['organization_id'])
    
    # Generate token
    access_token = create_access_token(identity=str(user['_id']))
    
    return jsonify({
        'message': 'User registered successfully',
        'token': access_token,
        'user': {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'organization': {
                'id': str(org_data['_id']),
                'name': org_data['name']
            }
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login for both user types"""
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Email and password required'}), 400
    
    # Find user
    user = User.find_by_email(data['email'])
    
    if not user or not User.verify_password(user, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Get organization details if any
    org = None
    if user.get('organization_id'):
        org_data = Organization.get_organization_by_id(user['organization_id'])
        if org_data:
            org = {
                'id': str(org_data['_id']),
                'name': org_data['name']
            }
    
    # Generate token
    access_token = create_access_token(identity=str(user['_id']))
    
    # Ensure we always return organization field (even if null)
    user_response = {
        'id': str(user['_id']),
        'name': user['name'],
        'email': user['email'],
        'role': user['role'],
        'organization': org  # This will be null if no org selected
    }
    
    return jsonify({
        'message': 'Login successful',
        'token': access_token,
        'user': user_response
    }), 200

@auth_bp.route('/select-organization', methods=['POST'])
@jwt_required
def select_organization():
    """Regular user selects organization after registration"""
    data = request.get_json()
    
    if 'organization_id' not in data:
        return jsonify({'error': 'Organization ID required'}), 400
    
    current_user = request.current_user
    
    # Check if user is regular
    if current_user['role'] != 'regular':
        return jsonify({'error': 'Only regular users can select organizations'}), 403
    
    # Verify organization exists
    org = Organization.get_organization_by_id(data['organization_id'])
    if not org:
        return jsonify({'error': 'Organization not found'}), 404
    
    # Update user with organization
    User.update_organization(str(current_user['_id']), data['organization_id'])
    
    # Get updated user
    updated_user = User.find_by_id(str(current_user['_id']))
    
    # Generate new token with updated info
    access_token = create_access_token(identity=str(updated_user['_id']))
    
    # Prepare response
    user_response = {
        'id': str(updated_user['_id']),
        'name': updated_user['name'],
        'email': updated_user['email'],
        'role': updated_user['role'],
        'organization': {
            'id': str(org['_id']),
            'name': org['name']
        }
    }
    
    return jsonify({
        'message': 'Organization selected successfully',
        'token': access_token,
        'user': user_response
    }), 200