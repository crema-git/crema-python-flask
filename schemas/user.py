from ma import ma
from models.user import UserModel
from marshmallow import (
    fields,
    validate, EXCLUDE
)


class UserSchema(ma.SQLAlchemyAutoSchema):
    email = fields.Str(
        required=True, validate=validate.Email(error="Not a valid email address")
    )

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True
        unknown = EXCLUDE
