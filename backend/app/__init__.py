from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
    r"/api/*": {
        "origins": ["chrome-extension://*", "http://localhost:*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

    app.config['SECRET_KEY'] = 'dev'
    app.config['DEBUG'] = True

    from app import routes
    app.register_blueprint(routes.main)

    return app 