import os
from flask import Flask
from config import SECRET_KEY
from database import init_db
from routes import register_routes

app = Flask(__name__)
app.secret_key = SECRET_KEY

register_routes(app)

if __name__ == '__main__':
    init_db()
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug)
