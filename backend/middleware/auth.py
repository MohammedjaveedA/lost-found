from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def jwt_required(f):
    """Custom JWT decorator that also adds user to request context"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.find_by_id(user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
            request.current_user = current_user
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
            
    return decorated_function

def org_admin_required(f):
    """Decorator to ensure user is an organization admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.find_by_id(user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
            if current_user['role'] != 'org_admin':
                return jsonify({'error': 'Organization admin access required'}), 403
                
            request.current_user = current_user
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
            
    return decorated_function