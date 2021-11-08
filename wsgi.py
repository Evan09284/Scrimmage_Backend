from app import create_app
from flask_redis import FlaskRedis
import os

app = create_app()
rd = FlaskRedis(app)

if __name__ == "__main__":
    port = os.environ.get("PORT") or 5000
    app.run(host="0.0.0.0", port=port, debug=True)
