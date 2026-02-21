from datetime import datetime
import re

def validate_email(email):
    """Basic email validation"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def format_date(date_str):
    """Convert string to datetime"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except:
        return None

def objectid_to_str(obj):
    """Convert ObjectId to string in dict"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == '_id':
                obj['id'] = str(value)
                del obj['_id']
            elif isinstance(value, dict):
                objectid_to_str(value)
            elif isinstance(value, list):
                for item in value:
                    objectid_to_str(item)
    return obj