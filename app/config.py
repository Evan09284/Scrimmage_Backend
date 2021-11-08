import os
from dotenv import load_dotenv
from flask_redis.client import FlaskRedis
from flask_socketio import SocketIO


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

rd = FlaskRedis()
socketio = SocketIO()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

SPORTSRADAR_KEY = os.environ.get('SPORTSRADAR_KEY')
META_KEY = os.environ.get('META_KEY')
