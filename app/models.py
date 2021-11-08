import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import backref
from sqlalchemy.sql.sqltypes import DateTime

db = SQLAlchemy()


class FiltersEnum(enum.Enum):
    __tablename__ = 'filters'

    football = "football"
    basketball = "basketball"
    baseball = "baseball"
    hockey = "hockey"
    tennis = "tennis"
    golf = "golf"
    esports = "esports"
    fighting = "fighting"


    @staticmethod
    def as_list():
        return [FiltersEnum.football.value, FiltersEnum.basketball.value, \
                FiltersEnum.baseball.value,  FiltersEnum.hockey.value, FiltersEnum.tennis.value, \
                FiltersEnum.golf.value, FiltersEnum.esports.value, FiltersEnum.fighting.value]


class ResultsEnum(enum.Enum):
    __tablename__ = 'results'

    win = "win"
    loss = "loss"
    push = "push"
    cancelled = "cancelled"

    @staticmethod
    def as_list():
        return [ResultsEnum.win.value, ResultsEnum.loss.value, \
            ResultsEnum.push.value, ResultsEnum.cancelled.value]


class NotificationStatusEnum(enum.Enum):
    __tablename__ = 'statuses'

    inactive = "inactive"
    scheduled = "scheduled"
    notified = "notified"

    @staticmethod
    def as_list():
        return [NotificationStatusEnum.inactive.value, NotificationStatusEnum.scheduled.value, \
                NotificationStatusEnum.notified.value]


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, nullable = False, unique = True)
    subscribed_ids = db.Column(ARRAY(db.String), default = None, unique = False) #blogs subscribed - saves author id
    newsfeed_filters = db.Column((ARRAY(ENUM(FiltersEnum))))
    light_mode = db.Column(db.Boolean, default=True) #default light mode
    odds_format = db.Column(db.Boolean, default=True) #default American
    stripe_id = db.Column(db.Integer, unique=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=DateTime)

    user_bets = db.relationship('UserBet', backref='user', lazy='joined')
    author = db.relationship('Author', backref='user', lazy='joined')


    def __repr__(self):
        return '<User {}>'.format(self.as_dict())


    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'subscribed_ids': self.subscribed_ids,
            'newsfeed_filters': self.newsfeed_filters,
            'light_mode': self.light_mode,
            'odds_format': self.odds_format,
            'stripe_id': self.stripe_id,
            'author_id': self.author_id
        }


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    subscribers = db.Column(ARRAY(db.String), default = []) #array of user_id
    email_subscribers = db.Column(ARRAY(db.String), default = [])
    total_revenue = db.Column(db.Integer) #ads + subscribers
    monthly_fee = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    posts = db.relationship('Post', backref='author', lazy='joined')


    def __repr__(self):
        return '<Author {}>'.format(self.as_dict())


    def as_dict(self):
        return {
            'id': self.id,
            'subscribers': self.subscribers,
            'email_subscribers': self.email_subscribers,
            'total_revenue': self.total_revenue,
            'monthly_fee': self.monthly_fee
        }


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    views = db.Column(db.Integer)
    original_post = db.Column(db.Text)
    post_edits = db.Column(ARRAY(db.String), default=[])
    free = db.Column(db.Boolean, default=False)
    revenue = db.Column(db.Integer, default=0) #algorithm for percentage paid
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=DateTime)


    def __repr__(self):
        return '<Post {}>'.format(self.as_dict())


    def as_dict(self):
        return {
            'id': self.id,
            'views': self.views,
            'original_post': self.original_post,
            'post_edits': self.post_edits,
            'free': self.free,
            'revenue': self.revenue,
            'author_id': self.author_id
        }


class UserBet(db.Model):
    __tablename__ = 'user_bets'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String)
    american_odds = db.Column(db.Integer)
    decimal_odds = db.Column(db.Integer)
    stake = db.Column(db.Integer)
    sportsbook = db.Column(db.String(50))
    handicap = db.Column(db.Integer)
    notification_handicap = db.Column(db.Numeric(3,1))
    notification_price = db.Column(db.Integer)
    closing_line_value = db.Column(db.Numeric(4,4))
    roi = db.Column(db.Numeric (4,4))
    results = db.Column((ARRAY(ENUM(ResultsEnum))))
    payout = db.Column(db.Numeric(4,4))
    game_date = db.Column(db.DateTime)
    bet_date = db.Column(db.DateTime)
    active_wager = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notification_status = db.Column((ARRAY(ENUM(NotificationStatusEnum))))

    # def __repr__(self):
    #     return '<UserBet {}>'.format(self.as_dict())

    def as_dict(self):
        return {
            'id': self.id,
            'event': self.event,
            'american_odds': self.american_odds,
            'decimal_odds': self.decimal_odds,
            'stake': self.stake,
            'sportsbook': self.sportsbook,
            'handicap': self.handicap,
            'notification_handicap': float(self.notification_handicap),
            'notification_price': self.notification_price,
            'notification_status': self.notification_status,
            'closing_line_value': float(self.closing_line_value),
            'return_on_investment': float(self.roi),
            'win_or_loss': self.results,
            'payout': float(self.payout),
            'game_date': self.game_date,
            'bet_date': self.bet_date,
            'game_date': self.game_date,
            'bet_date': self.bet_date,
            'active_wager': self.active_wager,
            'user_id': self.user_id
        }
