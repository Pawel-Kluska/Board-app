from urllib import request

from flask import Blueprint, flash, redirect, render_template, url_for, abort
from flask_login import login_required, current_user
from src import db

from src.models import Post, Like, Comment
from src.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)

"""Endpoints related to posts and comments"""


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """Endpoint displaying form to create new post, validating data and saving it in database"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author_post=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post added', 'success')
        return redirect(url_for('main.home'))
    return render_template('post/post_form.html', title='Post', form=form)


@posts.route('/post/<post_id>', methods=['GET'])
@login_required
def post(post_id):
    """Endpoint displaying one, chosen post by id"""
    post_db = Post.query.get_or_404(post_id)
    return render_template('post/post.html', title=post_db.title, post=post_db)


@posts.route('/post/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """Endpoint displaying form to update post and carrying out this update"""
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
        return redirect(url_for('posts.post', post_id=post_db.id))
    elif request.method == 'GET':
        form.title.data = post_db.title
        form.content.data = post_db.content

    return render_template('post/post_form.html', title='Update Post', form=form)


@posts.route('/post/<post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Endpoint removing chosen post"""
    post_db = Post.query.get_or_404(post_id)
    if post_db.author_post != current_user:
        abort(403)

    db.session.delete(post_db)
    db.session.commit()
    flash('Post deleted', 'success')

    return redirect(url_for('main.home'))


@posts.route('/new_comment/<post_id>', methods=['POST'])
def new_comment(post_id):
    """endpoint saving new comments"""
    form = CommentForm()
    if form.validate_on_submit():
        author_post = Post.query.filter_by(id=post_id).first()
        comment = Comment(content=form.content.data, author_comment=current_user, post=author_post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added', 'success')
        return redirect(url_for('main.home'))


@posts.route('/like/<post_id>/<value>', methods=['GET', 'POST'])
@login_required
def like(post_id, value):
    """Endpoint saving new likes or dislikes for specific post.
    User can like or dislike a lot of posts, but he can't like or dislike one post a few times
     If user has liked a post, and he clicks on dislike he changes his record in database
     If user clicks on like/dislike which already is in database, he removes his record"""

    if value == 'True':
        value = True
    else:
        value = False

    db_post = Post.query.filter_by(id=int(post_id)).first()
    db_like = Like.query.filter_by(author_like=current_user, post=db_post).first()

    if db_like:
        if not value and db_like.like_value or value and not db_like.like_value:
            db_like.like_value = value
        else:
            db.session.delete(db_like)

    else:
        new_like = Like(like_value=value, author_like=current_user, post=db_post)
        db.session.add(new_like)
    db.session.commit()
    return redirect(url_for('main.home'))
