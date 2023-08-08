from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

# Stocks blueprint
stocks_bp = Blueprint('stocks', 'stocks', url_prefix='/stocks', description='Stocks endpoints')

@stocks_bp.route('/hello')
class HelloWorldResource(MethodView):
    @jwt_required()
    @stocks_bp.response(200)
    def get(self):
        # current_user = get_jwt_identity()
        return "hello world"