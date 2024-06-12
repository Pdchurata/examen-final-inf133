from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.services.auth_service import create_token, get_current_user
from app.utils.decorators import admin_required

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/', methods=['GET'])
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/<int:id>', methods=['GET'])
@admin_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        role=data.get('role', 'customer')
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']
    user.phone = data['phone']
    user.role = data.get('role', user.role)
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        token = create_token(user)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/profile', methods=['GET'])
def profile():
    user = get_current_user()
    return jsonify(user.to_dict())
