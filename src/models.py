from flask_login import UserMixin
from flask import current_app
from src import db, login_manager
import jwt
import datetime

"""Models used to save data in database
Relational database has been used, the following relations occurred:
User can make a few posts, post has only one author
User can make a few comments under the post and he can make comments uder a few posts
Post has a lot of comments, comment has only one post and one author
User can like post only once, but he can like a lot of posts
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User model, it is used to log in"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(12), nullable=True)

    posts = db.relationship('Post', backref='author_post', lazy=True)
    likes = db.relationship('Like', backref='author_like', lazy=True)
    comments = db.relationship('Comment', backref='author_comment', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image_file})'

    def generate_confirmation_token(self, expiration=1800):
        """Function generating token used in changing password by email, it expires after 30 minutes"""
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    @staticmethod
    def confirm(token):
        """Function checking if token is correct and returning user"""
        try:
            token_data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None

        return User.query.get(token_data['user_id'])


class Post(db.Model):
    """Post model saved in database"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', cascade='all,delete', lazy=True)
    likes = db.relationship('Like', backref='post', cascade='all,delete', lazy=True)

    def __repr__(self):
        return f'Post({self.title}, {self.content})'


class Comment(db.Model):
    """Comment model saved in database"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'Comment({self.author_comment, self.content})'


class Like(db.Model):
    """Like/dislike model: like_value=True - like, like_value=False - dislike"""
    id = db.Column(db.Integer, primary_key=True)

    like_value = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'Like({self.like_value}, {self.author_like}, {self.post})'
