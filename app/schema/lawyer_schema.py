from marshmallow import Schema, fields


class LawyerSchema(Schema):
    id = fields.Integer(required=True)
    admin_id = fields.Integer(required=True)
    name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        ordered = True


class LawyerCreateSchema(LawyerSchema):
    class Meta:
        fields = ["id", "admin_id", "name", "username", "email", "password"]
        exclude = ["id", "admin_id"]


class LawyerReadSchema(LawyerSchema):
    class Meta:
        fields = ["id", "admin_id", "name", "username", "email", "password"]
        load_only = ["password"]


class LawyerSigninSchema(LawyerSchema):
    class Meta:
        fields = ["id", "admin_id", "name", "username", "email", "password"]
        exclude = ["id", "admin_id", "name", "email"]
