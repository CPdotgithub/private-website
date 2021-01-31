from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from celery import Celery
from flask_caching import Cache

bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

cache = Cache()

CELERY_BROKER_URL = 'redis://:'+os.getenv('redis_password')+'@127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://:'+os.getenv('redis_password')+'@127.0.0.1:6379/1'

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)




@login_manager.user_loader
def load_user(user_id):
    from cpblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
