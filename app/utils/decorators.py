from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from app.models.user import User

def role_required(role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user.role != role:
                return jsonify({"message": "Access denied"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

admin_required = role_required('admin')
customer_required = role_required('customer')
