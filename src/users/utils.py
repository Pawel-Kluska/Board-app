import os
import secrets
from flask_mail import Message

import PIL.Image
from src import mail
from flask import url_for, current_app

"""Utility functions made by user"""


def save_picture(form_picture):
    """Function saving picture in static/profile_img folder
    It hashes picture names because in folder they has to be unique"""
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_img', picture_fn)

    output_size = (125, 125)
    image = PIL.Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fn


def send_email(user):
    """Function sending email to user who requested change password
    It sends token with it which expires after 30 minutes"""
    token = user.generate_confirmation_token()
    msg = Message('Password Reset Request', sender='boardapp.flask@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password visit the following website {url_for('users.reset_password', token=token, _external=True)}
'''
    mail.send(msg)
