from datetime import datetime

from flask_login import UserMixin

from flaskblog import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='img.jpg')
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(12), nullable=True)
    phone = db.Column(db.String(12), nullable=True)

    posts = db.relationship('Post', backref='author_post', lazy=True)
    comments = db.relationship('Comment', backref='author_comment', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image})'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f'Post({self.title}, {self.date})'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'Post({self.title}, {self.date})'
