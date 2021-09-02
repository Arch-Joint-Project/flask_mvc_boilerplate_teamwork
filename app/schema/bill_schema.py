from marshmallow import Schema, fields


class BillSchema(Schema):
    id = fields.Integer(required=True)
    lawyer_id = fields.Integer(required=True)
    billable_rate = fields.Integer(required=True)
    company = fields.String(required=True)
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)

    class Meta:
        ordered = True


class BillCreateSchema(BillSchema):
    class Meta:
        fields = ["id", "lawyer_id", "billable_rate", "company", "date", "start_time",
                  "end_time"]
        exclude = ["id", "lawyer_id"]


class BillUpdateSchema(BillSchema):
    class Meta:
        fields = ["id", "lawyer_id", "billable_rate", "company", "date", "start_time",
                  "end_time"]
        exclude = ["id", "lawyer_id", "company"]


class BillReadSchema(BillSchema):
    class Meta:
        fields = ["id", "lawyer_id", "billable_rate", "company", "date", "start_time",
                  "end_time"]


class BillDeleteSchema(BillSchema):
    pass


class InvoiceSchema(BillSchema):
    class Meta:
        fields = ["id", "billable_rate", "company", "start_time",
                  "end_time"]
