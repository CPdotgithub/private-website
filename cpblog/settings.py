import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY",os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.path.join(os.getenv('DATABASE_URI'),'test')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER='smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME','1633477479@qq.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('cp1994','1633477479@qq.com')
    CPBLOG_MAIL_SUBJECT_PREFIX = "CP-Home"
    CPBLOG_EMAIL = os.getenv('MAIL_SENDER')
    CPBLOG_POST_PER_PAGE = 10
    CPBLOG_MANAGE_POST_PER_PAGE = 15
    CPBLOG_COMMENT_PER_PAGE = 15
    CPBLOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    BOOTSTRAP_SERVE_LOCAL = True
    DATABASE_QUERY_TIMEOUT = 1


    CPBLOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    CPBLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']



class DevelopmentConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = os.path.join(os.getenv('DATABASE_URI'),'development')

class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'







class  TestConfig(BaseConfig):
    Testing = True
    WTF_CRSF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.path.join(os.getenv('DATABASE_URI'),'test')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.path.join(os.getenv('DATABASE_URI'),'data')

config = {
    'development':DevelopmentConfig,
    'test':TestConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}