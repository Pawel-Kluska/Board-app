from flask_login import current_user

from src.models import Like, Post, User


def get_posts_ordered(page, per_page, user=None, default_order=1):

    if default_order == 1:
        posts = Post.query.order_by(Post.date.desc())

    elif default_order == 2:
        posts = Post.query.order_by(Post.date)

    elif default_order == 3:
        posts = Post.query.join(User).order_by(User.username)

    elif default_order == 4:
        posts = Post.query.order_by(Post.title)
    else:
        posts = Post.query

    if user is not None and default_order != 3:
        posts = posts.filter_by(author_post=user)

    posts = posts.paginate(page=page, per_page=per_page)
    return posts


def get_post_likes(post_l, type_like):
    if type_like == '1':
        return len(list(filter(lambda l: l.like_value is True, post_l.likes)))
    elif type_like == '0':
        return len(list(filter(lambda l: l.like_value is False, post_l.likes)))
    else:
        return None


def is_liked(db_post, value):
    db_like = Like.query.filter_by(author_like=current_user, post=db_post).first()
    if value == '0' and db_like is not None and not db_like.like_value:
        return True
    elif value == '1' and db_like is not None and db_like.like_value:
        return True
    else:
        return False
