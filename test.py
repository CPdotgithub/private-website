from cpblog.emails import send_confirm_email
from cpblog.utils import generate_token,validate_token
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os

SECRET_KEY = os.getenv('SECRET_KEY','fdsfdsfdsaf45656#$')
s = Serializer(SECRET_KEY, expires_in=3600)
data = {'id': 'CP', 'operation': operation}
token = s.dumps(data)