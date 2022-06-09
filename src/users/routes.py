from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from src import db, bcrypt

from src.models import User
from src.users.forms import RegistrationForm, LoginForm, AccountForm, PasswordForm, PasswordResetReqForm, ResetPassword
from src.users.utils import save_picture, send_email

users = Blueprint('users', __name__)

"""Endpoints related to users"""


@users.route('/register', methods=['GET', 'POST'])
def register():
    """Endpoint displaying register form and handling this registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    address=form.address.data,
                    phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}. You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('user/registration.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """Endpoint displaying login form and handling this logging"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    """Endpoint used to log out user"""
    logout_user()
    flash(f'You logged out properly', 'success')
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """Endpoint displaying update form and handling this update"""
    img = url_for('static', filename='profile_img/' + current_user.image_file)
    form_user = AccountForm()
    form_password = PasswordForm()
    # Data form
    if form_user.submit1.data and form_user.validate():
        if form_user.picture.data:
            picture_file = save_picture(form_user.picture.data)
            current_user.image_file = picture_file
        current_user.username = form_user.username.data
        current_user.email = form_user.email.data
        current_user.address = form_user.address.data
        current_user.phone = form_user.phone.data
        db.session.commit()
        flash('Update succesful', 'success')
        return redirect(url_for('users.account'))
    # Password form
    if form_password.submit2.data and form_password.validate():
        if bcrypt.check_password_hash(current_user.password, form_password.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form_password.password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed succesfully', 'success')
            return redirect(url_for('main.home'))
        flash('You entered wrong password, try again', 'danger')

    form_user.username.data = current_user.username
    form_user.email.data = current_user.email
    form_user.address.data = current_user.address
    form_user.phone.data = current_user.phone
    return render_template('user/account_form.html', title='Account', image=img,
                           form_user=form_user, form_password=form_password)


@users.route('/request_reset', methods=['GET', 'POST'])
def request_reset():
    """Endpoint displaying request reset password form and sending email on entered address"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = PasswordResetReqForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('Email has been sent', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/request_reset_form.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Endpoint displaying password form and handling this change (after clicking on link received in email"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.confirm(token)
    if user is None:
        flash("Invalid token", 'warning')
        return redirect(url_for('users.request_reset'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password updated. You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_password.html', title='Reset Password', form=form)
