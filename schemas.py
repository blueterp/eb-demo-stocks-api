from marshmallow import Schema, fields

class RegisterSchema(Schema):
    name = fields.String(required=True, load_only=True)
    email = fields.Email(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)

class LoginSchema(Schema):
    name = fields.String(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)

class LoginSuccessSchema(Schema):
    access_token = fields.String(required=True)

