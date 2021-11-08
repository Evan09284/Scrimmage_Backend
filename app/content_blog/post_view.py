import flask
from flask import Blueprint
from flask_cors import cross_origin


#individual post view

post_view_bp = Blueprint('post_view', __name__, url_prefix = '/content_blog')


@post_view_bp.route('/<int:post_id>')
def get_post():
    return 'get request to retrieve single post from db'