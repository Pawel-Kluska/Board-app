from flask_login import UserMixin

from src import db, login_manager, app
import jwt
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(12), nullable=True)
    phone = db.Column(db.String(12), nullable=True)

    posts = db.relationship('Post', backref='author_post', lazy=True)
    likes = db.relationship('Like', backref='author_like', lazy=True)
    comments = db.relationship('Comment', backref='author_comment', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.image_file})'

    def generate_confirmation_token(self, expiration=1800):
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    @staticmethod
    def confirm(token):
        try:
            token_data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None

        return User.query.get(token_data['user_id'])


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', cascade='all,delete', lazy=True)
    likes = db.relationship('Like', backref='post', cascade='all,delete', lazy=True)

    def __repr__(self):
        return f'Post({self.title}, {self.date})'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'Comment({self.content})'


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    like_value = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'Like({self.like_value}, {self.user_id}, {self.post_id})'

