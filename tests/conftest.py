import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def base_url():
    return 'http://127.0.0.1:5000'


@pytest.fixture
def get_bet_url(base_url):
    return base_url+'/betting/1' # 1 = User ID


@pytest.fixture
def post_bet_url(base_url):
    return base_url+'/betting'
