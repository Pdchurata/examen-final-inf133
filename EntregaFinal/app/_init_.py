from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.controllers import (
        restaurant_controller,
        reservation_controller,
        user_controller
    )
    app.register_blueprint(restaurant_controller.bp)
    app.register_blueprint(reservation_controller.bp)
    app.register_blueprint(user_controller.bp)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Restaurant Reservation API"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
