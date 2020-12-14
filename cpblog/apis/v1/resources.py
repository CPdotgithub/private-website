from flask import jsonify, request, current_app, url_for, g
from flask.views import MethodView

from cpblog.apis.v1 import api_v1
from cpblog.apis.v1.auth import auth_required, generate_token
from cpblog.apis.v1.errors import api_abort, ValidationError
from cpblog.apis.v1.schemas import user_schema, item_schema, items_schema
from cpblog.extensions import db
from cpblog.models import Account,Order,LoanOrder


def get_item_body():
    data = request.get_json()
    body = data.get('body')
    if body is None or str(body).strip() == '':
        raise ValidationError('The item body was empty or invalid.')
    return body

class IndexAPI(MethodView):
    
    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://cp1994.work/api/v1",
            "current_user_url": "http://cp1994.work/api/v1/user",
            "authentication_url": "http://cp1994.work/api/v1/token",
            "item_url": "http://cp1994.work/api/v1/items/{item_id }",
            "current_user_items_url": "http://cp1994.work/api/v1/user/items{?page,per_page}",
            "current_user_active_items_url": "http://cp1994.work/api/v1/user/items/active{?page,per_page}",
            "current_user_completed_items_url": "http://cp1994.work/api/v1/user/items/completed{?page,per_page}",
        })


class AuthTokenAPI(MethodView):

    def post(self):
        grant_type = request.form.get('grant_type')
        username = request.form.get('username')
        password = request.form.get('password')

        if grant_type is None or grant_type.lower() != 'password':
            return api_abort(code=400, message='The grant type must be password.')


        user = Account.query.filter_by(username=username).first()
        if user is None or not user.validate_password(password):
            return api_abort(code=400, message='Either the username or password was invalid.')

        token, expiration = generate_token(user)

        response = jsonify({
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': expiration
        })
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        return response


class StockDataAPI(MethodView):
    decorators = [auth_required]

    def get(self, code,start_date,end_date,frequency,adjustflag):
        """Get item."""
        user = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        return jsonify(item_schema(item))

class OrderAPI(MethodView):
    decorators = [auth_required]
    def get(self,order_id):
        user = Order.query.get_or_404(order_id)
        if g.current_user != order.user_id:
            return api_abort(403)
        return jsonify(order_schema(order))
    
class AccountAPI(MethodView):
    decorators = [auth_required]
    def get(self, account_id):
       
        user = Account.query.get_or_404(account_id)
        if g.current_user != user.author:
            return api_abort(403)
        return jsonify(item_schema(item))

