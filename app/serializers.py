from marshmallow import fields, pre_load, Schema, validate, ValidationError


class UserSchema(Schema):
    class Meta:
        fields = ("email", "password")
        load_only = ("password", )

    email = fields.Email(required=True, validate=[validate.Length(max=50)])
    password = fields.Str(
        required=True,
        validate=[validate.Length(min=5, max=70)]
    )

    # Check for empty payload.
    # We don't need to check for that scenario in enpoint anymore
    @pre_load
    def not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("No input data provided", "message")
        return data


class DataSchema(Schema):
    class Meta:
        fields = ("value", "unit", "created_on")
        dump_only = ("created_on",)

    value = fields.Int(required=True)
    unit = fields.Str(validate=[validate.Length(max=55)])
    created_on = fields.DateTime()

    @pre_load
    def not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("No input data provided", "message")
        return data
