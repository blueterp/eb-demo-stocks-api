from flask import Flask, request
from flask.views import MethodView

from flask_smorest import Api, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from schemas import RegisterSchema, LoginSchema, LoginSuccessSchema
from auth import auth_bp
from stocks import stocks_bp
from auth import blocklist

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    # print(jwt_header)
    # print(jwt_payload)
    jti = jwt_payload["jti"]
    return jti in blocklist

api = Api(app)

api.register_blueprint(stocks_bp)
api.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)