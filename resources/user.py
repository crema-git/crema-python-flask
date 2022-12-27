from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST

USER_ALREADY_EXISTS = "A user with that email already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={}> successfully logged out."
INTERNAL_SERVER_ERROR = "!Oops, something went wrong"
user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            user_json = request.get_json()
            user = user_schema.load(user_json)

            if UserModel.find_by_email(user.email):
                return {"error": USER_ALREADY_EXISTS}, 400

            user.save_to_db()

            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"token": access_token, "refresh_token": refresh_token}, 200
        except:
            return {"error": INTERNAL_SERVER_ERROR}, 500


# class User(Resource):


# @classmethod
# def delete(cls, user_id: int):
#     user = UserModel.find_by_id(user_id)
#     if not user:
#         return {"message": USER_NOT_FOUND}, 404
#
#     user.delete_from_db()
#     return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            user_json = request.get_json()
            user_data = user_schema.load(user_json, partial=("name",))

            user = UserModel.find_by_email(user_data.email)
            if user and safe_str_cmp(user_data.password, user.password):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"token": access_token, "refresh_token": refresh_token}, 200

            return {"error": INVALID_CREDENTIALS}, 400
        except Exception as e:
            return {"error": INTERNAL_SERVER_ERROR}, 500

    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        return user_schema.dump(user), 200


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
