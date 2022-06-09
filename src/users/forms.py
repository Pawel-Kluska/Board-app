from src import bcrypt
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from src.models import User

"""Some forms used by user"""


class RegistrationForm(FlaskForm):
    """Form used by user to register"""
    username = StringField('Username', validators=[DataRequired(), Length(2, 30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[Length(0, 12)])
    phone = StringField('Phone', validators=[Length(9, 12)])
    terms_of_service = BooleanField('Terms of service', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        """Function checking if user exists in database"""
        user_db = User.query.filter_by(username=username.data).first()
        if user_db:
            raise ValidationError('User already exists')

    def validate_email(self, email):
        """Function checking if email exists in database"""
        email_db = User.query.filter_by(email=email.data).first()
        if email_db:
            raise ValidationError('Email already exists')

    def validate_password(self, password):
        """Function checking if password is correct. It has to have 8 chars, one special character and one number"""
        if not any(not c.isalnum() for c in password.data):
            raise ValidationError('Password must contain at least one special character')
        if not any(char.isdigit() for char in password.data):
            raise ValidationError('Password must contain at least one number')
        password_db = User.query.filter_by(
            password=bcrypt.generate_password_hash(password.data).decode('utf-8')).first()
        if password_db:
            raise ValidationError('You can\'t enter previous password')


class LoginForm(FlaskForm):
    """Form used by user to log in into app"""
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField("Remember me")

    submit = SubmitField('Login')


class AccountForm(FlaskForm):
    """Form used by user to update user account"""
    username = StringField('Username', validators=[DataRequired(), Length(2, 30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[Length(0, 12)])
    picture = FileField('Update picture', validators=[FileAllowed(['jpg', 'png'])])
    phone = StringField('Phone', validators=[Length(9, 12)])
    submit1 = SubmitField('Update user')

    def validate_username(self, username):
        """Function checking if user exists in database"""
        if current_user.username != username.data:
            user_db = User.query.filter_by(username=username.data).first()
            if user_db:
                raise ValidationError('User already exists')

    def validate_email(self, email):
        """Function checking if email exists in database"""
        if current_user.email != email.data:
            email_db = User.query.filter_by(email=email.data).first()
            if email_db:
                raise ValidationError('User already exists')


class PasswordForm(FlaskForm):
    """Form used by user to change password"""
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit2 = SubmitField('Update Password')


class PasswordResetReqForm(FlaskForm):
    """Function used to request changing password by email"""
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Reset')

    def validate_email(self, email):
        """Checking if email is correct"""
        email_db = User.query.filter_by(email=email.data).first()
        if email_db is None:
            raise ValidationError('Email doesn\'t exists')


class ResetPassword(FlaskForm):
    """Form used by user to reset password (after email request)"""
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')
