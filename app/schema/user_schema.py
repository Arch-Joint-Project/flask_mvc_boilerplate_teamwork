from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    age = fields.Integer(required=True)
    date_of_birth = fields.Date(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

    class Meta:
        ordered = True


class UserCreateSchema(UserSchema):
    class Meta:
        fields = ["id", "first_name", "last_name", "username", "email", "age",
                  "date_of_birth", "password"]


class UserUpdateSchema(UserSchema):
    class Meta:
        fields = ["id", "first_name", "last_name", "username", "email", "age",
                  "date_of_birth", "password"]


class UserReadSchema(UserSchema):
    class Meta:
        fields = ["id", "first_name", "last_name", "username", "email", "age",
                  "date_of_birth"]


class UserDeleteSchema(UserSchema):
    pass
















# from marshmallow import Schema, fields, validate
#
#
# class UserSchema(Schema):
#     id = fields.Int(required=True)
#     billable_rate = fields.Int(required=True)
#     company = fields.String(required=True)
#     date = fields.DateTime()
#     start_time = fields.DateTime()
#     end_time = fields.DateTime()
#
#
# class UserCreateSchema(Schema):
#     billable_rate = fields.Int(required=True)
#     company = fields.String(required=True)
#     date = fields.DateTime(required=True)
#     start_time = fields.DateTime(required=True)
#     end_time = fields.DateTime(required=True)
#
#     class Meta:
#         fields = ["billable_rate", "company", "date"]
#
#
# class UserUpdateSchema(Schema):
#     billable_rate = fields.Int()
#     company = fields.String()
#     date = fields.DateTime()
#
#     class Meta:
#         fields = ["billable_rate", "company", "date"]
