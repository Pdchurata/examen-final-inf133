from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models.user import User

def create_token(user):
    return create_access_token(identity=user.id)

@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)
