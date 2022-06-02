
class Config:
    SECRET_KEY = '58b35f5c02f37f5bd505bcb95d0433fe'
    SQLALCHEMY_DATABASE_URI = 'mysql://flask_user:flask_password@localhost/blog'
    #SQLALCHEMY_DATABASE_URI = 'mysql://bed4037b2e5cac:ebce9038@us-cdbr-east-05.cleardb.net/heroku_099311c585c25d1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'boardapp.flask@gmail.com'
    MAIL_PASSWORD = 'flask_password'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
