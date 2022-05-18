import os
import secrets

from PIL.Image import Image
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, AccountForm, PasswordForm
from flaskblog import app, db, bcrypt


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))

    return render_template('registration.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')

            next_page = request.args.get('next')
            print(type(next_page))
            print(next_page)

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You logged out properly', 'success')
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + ext
    picture_path = os.path.join(app.root_path, 'static/profile_img', picture_fn)

    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    img = url_for('static', filename='profile_img/' + current_user.image_file)
    form_user = AccountForm()
    form_password = PasswordForm()

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
        return redirect(url_for('account'))

    if form_password.submit2.data and form_password.validate():
        if bcrypt.check_password_hash(current_user.password, form_password.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form_password.password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed succesfully', 'success')
            return redirect(url_for('home'))
        flash('You entered wrong password, try again', 'danger')

    form_user.username.data = current_user.username
    form_user.email.data = current_user.email
    form_user.address.data = current_user.address
    form_user.phone.data = current_user.phone
    return render_template('account_form.html', title='Account', image=img,
                           form_user=form_user, form_password=form_password)
