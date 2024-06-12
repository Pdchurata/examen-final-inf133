from app import db
from datetime import datetime

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    reservation_date = db.Column(db.DateTime, default=datetime.utcnow)
    num_guests = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.String(500))
    status = db.Column(db.String(50), default='pending')

    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    restaurant = db.relationship('Restaurant', backref=db.backref('reservations', lazy=True))
