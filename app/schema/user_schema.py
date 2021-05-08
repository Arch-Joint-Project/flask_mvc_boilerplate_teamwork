from marshmallow import fields, Schema


class User(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()

    class Meta:
        fields = ["first_name", "last_name", "email"]


class UserCreate(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    class Meta:
        fields = ["first_name", "last_name", "email", "password"]


class UserLogin(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    class Meta:
        fields = ["email", "password"]


class AccessToken(Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()

    class Meta:
        fields = ["access_token", "refresh_token"]


class RefreshToken(Schema):
    refresh_token = fields.Str(required=True)
