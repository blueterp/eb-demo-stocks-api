from flask import Flask, request
from flask.views import MethodView

from flask_smorest import Api, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from schemas import RegisterSchema, LoginSchema, LoginSuccessSchema

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)
api = Api(app)



# Auth blueprint
auth_bp = Blueprint('auth', 'auth', url_prefix='/auth', description='Authentication endpoints')

users_db = {}
blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    # print(jwt_header)
    # print(jwt_payload)
    jti = jwt_payload["jti"]
    return jti in blocklist


def get_header(headers):
    bearer = headers.get('Authorization')    # Bearer YourTokenHere
    return bearer.split()[1]

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

# Stocks blueprint
stocks_bp = Blueprint('stocks', 'stocks', url_prefix='/stocks', description='Stocks endpoints')

@stocks_bp.route('/hello')
class HelloWorldResource(MethodView):
    @jwt_required()
    @stocks_bp.response(200)
    def get(self):
        # current_user = get_jwt_identity()
        return "hello world"
    
api.register_blueprint(stocks_bp)
api.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)