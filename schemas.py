from marshmallow import Schema, fields

class RegisterSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)

class LoginSchema(Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)
