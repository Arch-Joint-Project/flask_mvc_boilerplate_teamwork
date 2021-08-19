from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(required=True)
    billable_rate = fields.Int(required=True)
    company = fields.String(required=True)
    date = fields.DateTime()
    start_time = fields.DateTime()
    end_time = fields.DateTime()


class UserCreateSchema(Schema):
    billable_rate = fields.Int(required=True)
    company = fields.String(required=True)
    date = fields.DateTime(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)


    class Meta:
        fields = ["billable_rate", "company", "date"]


class UserUpdateSchema(Schema):
    billable_rate = fields.Int()
    company = fields.String()
    date = fields.DateTime()

    class Meta:
        fields = ["billable_rate", "company", "date"]
