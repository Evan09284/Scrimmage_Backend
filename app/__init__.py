import json
from flask import Flask, request
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_cors import cross_origin, CORS
from .config import Config, rd, socketio
from .home import home
from .user import login, sign_up, profile
from .content_blog.author import (
    author_dashboard, author_login, author_signup, create_post
)
from .content_blog import main_page, post_view
from .news import newsfeed
from .betting import bet_slip, tracker
from .betting.metabet import (
    odds, scores, side_odds, odds_timer
)
from .models import db
from flask_apscheduler import APScheduler


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    scheduler = APScheduler()
    scheduler.add_job(
        id="Update Odds Task", 
        func=odds_timer.update_odds,
        trigger='interval', 
        seconds=60
    )
    scheduler.add_job(
        id="Compare notification price",
        func=odds_timer.compare_notification_price,
        trigger='interval',
        seconds=60
    )
    scheduler.add_job(
        id="Notify about changed price",
        func=odds_timer.price_notifying,
        trigger='interval',
        seconds=10
    )
    scheduler.start()

    app.register_blueprint(home.home_bp)
    app.register_blueprint(login.login_bp)
    app.register_blueprint(sign_up.signup_bp)
    app.register_blueprint(profile.profile_bp)
    app.register_blueprint(author_dashboard.auth_dash_bp)
    app.register_blueprint(author_login.author_login_bp)
    app.register_blueprint(author_signup.author_signup_bp)
    app.register_blueprint(create_post.create_post_bp)
    app.register_blueprint(bet_slip.bet_slip_bp)
    app.register_blueprint(tracker.tracker_bp)
    app.register_blueprint(newsfeed.newsfeed_bp)
    app.register_blueprint(main_page.main_content_page_bp)
    app.register_blueprint(post_view.post_view_bp)
    app.register_blueprint(odds.odds_bp)
    app.register_blueprint(scores.scores_bp)
    app.register_blueprint(side_odds.side_odds_bp)

    rd.init_app(app)
    socketio.init_app(app)
    db.init_app(app)
    Migrate(app, db)

    return app
