import requests
from .mocks import (
    fake_new_bet,
    fake_bet_list
)


def test_get_bet(app, get_bet_url):
    """
        Check if the GET request returns status code 200 along with a list
        :param get_bet_url:
        :return:
    """
    response = requests.get(url=get_bet_url)    
    assert response.status_code == 200
    assert response.json() == fake_bet_list


def test_post_bet(app, post_bet_url):
    """
        Check if the POST request returns status code 201
        :param post_bet_url:
        :return:
    """
    response = requests.post(url=post_bet_url, data=fake_new_bet)
    assert response.status_code == 201
    # assert response.json() == fake_new_bet
