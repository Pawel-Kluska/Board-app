from flask import Blueprint, render_template, redirect, request

from src.main.utils import get_posts_ordered, is_liked, get_post_likes
from src.models import User, Post
from src.posts.forms import CommentForm

main = Blueprint('main', __name__)

# Variable responsible for remembering actual sorting configuration
default_order = 1

"""Endpoints related to main part of the application"""


@main.route('/')
@main.route('/home')
@main.route('/home/<username>')
def home(username=None):
    """Endpoint displaying home page with all posts, it has extra parameter (username)
    to use for filtering posts by users who created them
    All posts are paginated, one page has maximum 5 posts"""

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

    return render_template('home/home.html', title=title, posts=posts, len=last_page, form=form,
                           get_likes=get_post_likes,
                           is_liked=is_liked)


@main.route('/about')
def about():
    """Endpoint generating template with application info"""
    return render_template('home/about.html', title='About')


# Endpoint wyświetlający warunki użytkowania strony

@main.route('/terms_of_service')
def terms_of_service():
    """Endpoint generating template with terms of service"""
    return render_template('user/terms_of_service.html', title='Terms of service')


@main.route('/sort/<order>', methods=['GET', 'POST'])
def sort(order):
    """Endpoint saving chosen sorting, it comes back to request who called it"""
    global default_order
    order = int(order)
    default_order = order
    return redirect(request.referrer)
