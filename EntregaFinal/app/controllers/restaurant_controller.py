from flask import Blueprint, request, jsonify
from app import db
from app.models.restaurant import Restaurant
from app.utils.decorators import admin_required

bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@bp.route('/', methods=['GET'])
def list_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])

@bp.route('/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.to_dict())

@bp.route('/', methods=['POST'])
@admin_required
def create_restaurant():
    data = request.get_json()
    restaurant = Restaurant(
        name=data['name'],
        address=data['address'],
        city=data['city'],
        phone=data['phone'],
        description=data.get('description', ''),
        rating=data.get('rating', 0.0)
    )
    db.session.add(restaurant)
    db.session.commit()
    return jsonify(restaurant.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    data = request.get_json()
    restaurant.name = data['name']
    restaurant.address = data['address']
    restaurant.city = data['city']
    restaurant.phone = data['phone']
    restaurant.description = data.get('description', restaurant.description)
    restaurant.rating = data.get('rating', restaurant.rating)
    db.session.commit()
    return jsonify(restaurant.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204
