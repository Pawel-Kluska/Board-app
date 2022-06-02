
from flask import Blueprint, render_template, redirect, request

from src.main.utils import get_posts_ordered, is_liked, get_post_likes
from src.models import User, Post
from src.posts.forms import CommentForm

main = Blueprint('main', __name__)

default_order = 1


@main.route('/')
@main.route('/home')
@main.route('/home/<username>')
def home(username=None):
    per_page = 5
    page = request.args.get('page', 1, type=int)
    if username is not None:
        user = User.query.filter_by(username=username).first()
        title = 'Posts made by user: ' + user.username
    else:
        user = None
        title = 'Home'
    posts = get_posts_ordered(page, per_page, user=user, default_order=default_order)
    length = Post.query.count()
    if length == 0:
        last_page = 1
    else:
        last_page = ((length - 1) // per_page) + 1

    form = CommentForm()

    return render_template('home.html', title=title, posts=posts, len=last_page, form=form, get_likes=get_post_likes,
                           is_liked=is_liked)


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/terms_of_service')
def terms_of_service():
    return render_template('terms_of_service.html', title='Terms of service')


@main.route('/sort/<order>', methods=['GET', 'POST'])
def sort(order):
    global default_order
    order = int(order)
    default_order = order
    return redirect(request.referrer)
