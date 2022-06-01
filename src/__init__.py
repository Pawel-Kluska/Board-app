from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '58b35f5c02f37f5bd505bcb95d0433fe'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask_user:flask_password@localhost/blog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bed4037b2e5cac:ebce9038@us-cdbr-east-05.cleardb.net/heroku_099311c585c25d1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'boardapp.flask@gmail.com'
app.config['MAIL_PASSWORD'] = 'flask_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
from src import routes
