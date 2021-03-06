from   urllib.parse import urlparse,urljoin

from flask import request,redirect,url_for,current_app

from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from cpblog.extensions import db
from cpblog.models import Admin
from cpblog.settings import Operations





def generate_token(admin, operation, expires_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)

    data = {'id': admin.id, 'operation': operation,}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(admin, token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or admin.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        admin.confirmed_user(True)
    elif operation == Operations.RESET_PASSWORD:
        admin.set_password(new_password)
        
        
        
    elif operation == Operations.CHANGE_EMAIL:
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if Admin.query.filter_by(email=new_email).first() is not None:
            return False
        admin.email = new_email
    else:
        return False

    db.session.commit()
    return True


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['CPBLOG_ALLOWED_IMAGE_EXTENSIONS']