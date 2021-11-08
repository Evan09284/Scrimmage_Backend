
def fake_new_user():
    return {
            "username": "test_user",
            "email": "test_user@mail.com",
            "subscribed_ids": 0,
            "newsfeed_filters": "football",
            "light_mode": True,
            "odds_format": True,
            "stripe_id": 1,
            "author_id": 1
    }


def fake_new_bet():
    return {
        "id": 1,
        "event": "string",
        "american_odds": 0,
        "decimal_odds": 0,
        "stake": 0,
        "sportsbook": "string",
        "handicap": 0,
        "notification_handicap": 0,
        "notification_price": 0,
        "closing_line_value": 0,
        "roi": 0,
        "payout": 0,
        "results": [
            "win"
        ],
        "game_date": "2021-09-28T19:41:32.677Z",
        "bet_date": "2021-09-28T19:41:32.677Z",
        "user_id": 1
    }


def fake_bet_list():
    return [
                {
                    "id": 1,
                    "event": "string",
                    "american_odds": 0,
                    "decimal_odds": 0,
                    "stake": 0,
                    "sportsbook": "string",
                    "handicap": 0,
                    "notification_handicap": 0,
                    "notification_price": 0,
                    "closing_line_value": 0,
                    "roi": 0,
                    "payout": 0,
                    "results": [
                        "win"
                    ],
                    "game_date": "2021-09-28T19:41:32.677Z",
                    "bet_date": "2021-09-28T19:41:32.677Z",
                    "user_id": 1
                },
                {
                    "id": 2,
                    "event": "string",
                    "american_odds": 0,
                    "decimal_odds": 0,
                    "stake": 0,
                    "sportsbook": "string",
                    "handicap": 0,
                    "notification_handicap": 0,
                    "notification_price": 0,
                    "closing_line_value": 0,
                    "roi": 0,
                    "payout": 0,
                    "results": [
                        "win"
                    ],
                    "game_date": "2021-09-28T19:44:32.677Z",
                    "bet_date": "2021-09-28T19:44:32.677Z",
                    "user_id": 1
                },
    ]
