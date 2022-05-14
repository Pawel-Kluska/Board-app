from flask_login import login_user, current_user, logout_user, login_required

from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
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


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
