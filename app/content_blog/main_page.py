import json
from flask import Blueprint
from flask_cors import cross_origin


#change name to match frontend component - contentsplash default
#default or personalized
main_content_page_bp = Blueprint('content_page', __name__, url_prefix='/content_blog')

#one for subscribe, one for default, one for top paid, top free(default for non subscribeer)

@main_content_page_bp.route('')
def main_page():
    return ' get request to return main blog page - relies on data if subscriber/logged in or not'




