import json
from flask import Blueprint
from flask_cors import cross_origin

create_post_bp = Blueprint('create_posts', __name__, url_prefix='/author')

@create_post_bp.route('/create_post')
# @cross_origin(headers=['Content-Type', 'Authorization'])
def create_post():
    return 'create/edit/delete a post from here'



#edit post
@create_post_bp.route('/create_post/<int:post_id>')
# @cross_origin(headers=['Content-Type', 'Authorization'])
def edit_post():
    return 'retrieve post by id to edit'
