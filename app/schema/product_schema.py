from marshmallow import fields, Schema


class Product(Schema):
    name = fields.Str()
    price = fields.Int()
    seller = fields.Str()

