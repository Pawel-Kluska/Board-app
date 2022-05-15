from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import User


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(2, 30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[Length(0, 12)])
    phone = StringField('Phone', validators=[Length(9, 12)])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user_db = User.query.filter_by(username=username.data).first()
        if user_db:
            raise ValidationError('User already exists')

    def validate_email(self, email):
        email_db = User.query.filter_by(email=email.data).first()
        if email_db:
            raise ValidationError('User already exists')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField("Remember me")

    submit = SubmitField('Login')


class AccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(2, 30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[Length(0, 12)])

    phone = StringField('Phone', validators=[Length(9, 12)])
    submit = SubmitField('Update user')

    def validate_username(self, username):
        if current_user.username != username.data:
            user_db = User.query.filter_by(username=username.data).first()
            if user_db:
                raise ValidationError('User already exists')

    def validate_email(self, email):
        if current_user.email != email.data:
            email_db = User.query.filter_by(email=email.data).first()
            if email_db:
                raise ValidationError('User already exists')


class PasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Password')