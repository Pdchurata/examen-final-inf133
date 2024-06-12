from flask import Blueprint

bp = Blueprint('main', __name__)

from app.controllers import (
    restaurant_controller,
    reservation_controller,
    user_controller
)
