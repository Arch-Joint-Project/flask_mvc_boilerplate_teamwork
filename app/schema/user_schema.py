from app import ma
from marshmallow import validate, fields


class UserBase(ma.Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    password = fields.Str()

    class Meta:
        fields = ['first_name', 'last_name', 'email', 'password']


class CreateUserSchema(UserBase):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserSchema(UserBase):
    pass
