import flask
from flask import Blueprint
from flask_cors import cross_origin



#sits on homepage??
newsfeed_bp = Blueprint('newsfeed', __name__, url_prefix='/')


@newsfeed_bp.route('/newsfeed')
def feedly():
    return 'news feed comes from here - not standalone page reroute api to home'



