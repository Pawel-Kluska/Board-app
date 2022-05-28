import os
import secrets

import PIL.Image
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from src.models import User, Post, Comment
from flask import render_template, url_for, flash, redirect, request, abort
from src.forms import RegistrationForm, LoginForm, AccountForm, PasswordForm, PostForm, PasswordResetReqForm, \
    ResetPassword, CommentForm
from src import app, db, bcrypt, mail

default_order = 1


@app.route('/')
@app.route('/home/<order>')
@app.route('/home')
def home(order=1):
    per_page = 5
    order = int(order)
    page = request.args.get('page', 1, type=int)
    if order == 1:
        posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=per_page)

    elif order == 2:
        posts = Post.query.order_by(Post.date).paginate(page=page, per_page=per_page)

    elif order == 3:
        posts = Post.query.join(User).order_by(User.username).paginate(page=page, per_page=per_page)

    elif order == 4:
        posts = Post.query.order_by(Post.title).paginate(page=page, per_page=per_page)
    else:
        posts = Post.query.paginate(page=page, per_page=per_page)
    all_posts = Post.query.all()
    last_page = ((len(all_posts) - 1) // per_page) + 1
    print(last_page)
    form = CommentForm()

    return render_template('home.html', title='Home', posts=posts, len=last_page, form=form)



@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home', order=default_order))
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
        return redirect(url_for('home', order=default_order))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home', order=default_order))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You logged out properly', 'success')
    return redirect(url_for('home', order=default_order))


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
            return redirect(url_for('home', order=default_order))
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
        return redirect(url_for('home', order=default_order))
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

    return redirect(url_for('home', order=default_order))


@app.route('/user/<username>')
def user_post(username):
    per_page = 5
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author_post=user).paginate(page=page, per_page=per_page)
    all_posts = Post.query.all()
    last_page = len(all_posts) / per_page

    return render_template('user_post.html', title='Home', posts=posts, len=last_page, user=user)


def send_email(user):
    token = user.generate_confirmation_token()
    msg = Message('Password Reset Request', sender='boardapp.flask@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password visit the following website {url_for('reset_password', token=token, _external=True)}
'''
    mail.send(msg)

@app.route('/request_reset', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('home', order=default_order))
    form = PasswordResetReqForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('Email has been sent', 'success')
        return redirect(url_for('login'))
    return render_template('request_reset_form.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home', order=default_order))
    user = User.confirm(token)
    if user is None:
        flash("Invalid token", 'warning')
        return redirect(url_for('request_reset'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password updated. You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/new_comment/<post_id>', methods=['GET', 'POST'])
def new_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        print(form.content)
        author_post = Post.query.filter_by(id=post_id).first()
        comment = Comment(content=form.content.data, author_comment=current_user, post=author_post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added', 'success')
        return redirect(url_for('home', order=default_order))

