from flask import Flask
from flask_cors import CORS
from models import setup_db
from .routes import init_routes


def create_app(test_config=None):

    app = Flask("flaskr")

    if test_config is None:
        setup_db(app)
    else:
        setup_db(app, database_path=test_config.get('SQLALCHEMY_DATABASE_URI'))

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    init_routes(app)

    return app
