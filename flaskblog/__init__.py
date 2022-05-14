from flask import Flask
from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '58b35f5c02f37f5bd505bcb95d0433fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask_user:flask_password@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from flaskblog import routes