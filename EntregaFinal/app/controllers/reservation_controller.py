from flask import Blueprint, request, jsonify
from app import db
from app.models.reservation import Reservation
from app.utils.decorators import admin_required, customer_required

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@bp.route('/', methods=['GET'])
@admin_required
def list_reservations():
    reservations = Reservation.query.all()
    return jsonify([reservation.to_dict() for reservation in reservations])

@bp.route('/<int:id>', methods=['GET'])
def get_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    return jsonify(reservation.to_dict())

@bp.route('/', methods=['POST'])
@customer_required
def create_reservation():
    data = request.get_json()
    reservation = Reservation(
        user_id=data['user_id'],
        restaurant_id=data['restaurant_id'],
        reservation_date=data['reservation_date'],
        num_guests=data['num_guests'],
        special_requests=data.get('special_requests', ''),
        status=data.get('status', 'pending')
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify(reservation.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
@customer_required
def update_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    data = request.get_json()
    reservation.reservation_date = data['reservation_date']
    reservation.num_guests = data['num_guests']
    reservation.special_requests = data.get('special_requests', reservation.special_requests)
    reservation.status = data.get('status', reservation.status)
    db.session.commit()
    return jsonify(reservation.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
@customer_required
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    return '', 204
