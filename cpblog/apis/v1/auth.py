# _*_coding:utf-8 _*_

from functools import wraps
from flask import g,current_app,request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from cpblog.apis.v1.errors import api_abort,invalid_token,token_missing
from cpblog.models import Admin
  

def generate_token(admin):
    expiration = 3600
    s = Serializer(current_app.config["SECRET_KEY"],expires_in=expiration)
    token = s.dumps({"id":admin.id}).decode("ascii")
    return token ,expiration


def validate_token(token):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    except (BadSignature,SignatureExpired):
        return False
    admin = Admin.query.get(data["id"])
    if admin is None:
        return False
    g.current_user = admin
    return True

def get_token():
    if "Authorization" in request.headers:
        try:
            token_type,token = request.headers["Authorization"].split(None,1)
        except ValueError:
            token_type = token = None
    else:
        token_type = token = None
    return token_type,token

def auth_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token_type,token = get_token()

        if request.method != "OPTIONS":
            if token_type is None or token_type.low() != "bearer":
                return api_abort(400,"type error")
            if token is  None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args,**kwargs)
    return decorated 

