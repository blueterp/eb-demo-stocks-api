from flask import request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_smorest import Blueprint
from schemas import RegisterSchema, LoginSchema, LoginSuccessSchema



# Auth blueprint
auth_bp = Blueprint('auth', 'auth', url_prefix='/auth', description='Authentication endpoints')

users_db = {}
blocklist = set()

@auth_bp.route('/register')
class RegisterResource(MethodView):
    @auth_bp.arguments(RegisterSchema)
    @auth_bp.response(200)
    def post(self, args):
        name = args['name']
        email = args['email']
        password = args['password']

        if name in users_db:
            return {'message': 'Username already exists'}, 400

        users_db[name] = {
            'email': email,
            'password': password
        }

        return {'message': 'User registration successful'}, 200

@auth_bp.route('/login')
class LoginResource(MethodView):
    @auth_bp.arguments(LoginSchema)
    @auth_bp.response(200, LoginSuccessSchema)
    def post(self, args):
        name = args['name']
        password = args['password']

        if name not in users_db or users_db[name]['password'] != password:
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=name)
        return {'access_token': access_token}, 200
    
@auth_bp.route('/logout')
class LogoutResource(MethodView):
    @jwt_required()
    @auth_bp.response(200)
    def post(self):
        jti = get_jwt()["jti"]
        print(jti)
        blocklist.add(jti)
        return {'message':"Logged out successsfully."},200