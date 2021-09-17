from marshmallow import Schema, fields


class AdminSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        ordered = True


class AdminCreateSchema(AdminSchema):
    class Meta:
        fields = ["id", "name", "username", "email", "password"]
        exclude = ["id"]


class AdminReadSchema(AdminSchema):
    class Meta:
        fields = ["id", "name", "username", "email", "password"]
        load_only = ["password"]


class AdminSigninSchema(AdminSchema):
    class Meta:
        fields = ["id", "name", "username", "email", "password"]
        exclude = ["id", "name", "email"]


class AdminUpdateSchema(AdminSchema):
    class Meta:
        fields = ["id", "name", "username", "email", "password"]
        exclude = ["id"]
