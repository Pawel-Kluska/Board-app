from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

"""A few forms related to posts"""


class PostForm(FlaskForm):
    """Form used to create post"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    """Form used to create comment"""
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Add')
