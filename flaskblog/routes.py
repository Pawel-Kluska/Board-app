import os
import secrets

import PIL.Image
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, AccountForm, PasswordForm, PostForm
from flaskblog import app, db, bcrypt


@app.route('/')
@app.route('/home')
def home():
    per_page = 1
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=per_page)
    all_posts = Post.query.all()
    last_page = len(all_posts)/per_page

    return render_template('home.html', title='Home', posts=posts, len=last_page)


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
    image = PIL.Image.open(form_picture)
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


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author_post=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post added', 'success')
        return redirect(url_for('home'))
    return render_template('post_form.html', title='Post', form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post_db = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post_db.title, post=post_db)


@app.route('/post/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post_db = Post.query.get_or_404(post_id)
    form = PostForm()
    if post_db.author_post != current_user:
        abort(403)
    if form.validate_on_submit():
        post_db.title = form.title.data
        post_db.content = form.content.data
        db.session.add(post_db)
        db.session.commit()
        flash('Post added', 'success')
        return redirect(url_for('post', post_id=post_db.id))
    elif request.method == 'GET':
        form.title.data = post_db.title
        form.content.data = post_db.content

    return render_template('post_form.html', title='Update Post', form=form)


@app.route('/post/<post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post_db = Post.query.get_or_404(post_id)
    if post_db.author_post != current_user:
        abort(403)

    db.session.delete(post_db)
    db.session.commit()
    flash('Post deleted', 'success')

    return redirect(url_for('home', title='home'))


@app.route('/user/<username>')
def user_post(username):
    per_page = 1
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author_post=user).paginate(page=page, per_page=per_page)
    all_posts = Post.query.all()
    last_page = len(all_posts)/per_page

    return render_template('user_post.html', title='Home', posts=posts, len=last_page, user=user)