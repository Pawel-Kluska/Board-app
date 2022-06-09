"""Basic app configuration"""


class Config:
    SECRET_KEY = '58b35f5c02f37f5bd505bcb95d0433fe'
    # SQLALCHEMY_DATABASE_URI = 'mysql://flask_user:flask_password@localhost/blog'
    SQLALCHEMY_DATABASE_URI = 'mysql://b0c030fa740e0b:942a5ed3@eu-cdbr-west-02.cleardb.net/heroku_5567a239a35952c'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'boardapp.flask@gmail.com'
    MAIL_PASSWORD = 'vethbuywbcbpncjv'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
