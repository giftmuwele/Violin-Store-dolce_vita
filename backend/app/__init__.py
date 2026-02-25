from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import mysql, bcrypt
import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
    app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")

    return app


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    mysql.init_app(app)
    bcrypt.init_app(app)

    # -----------------------------------
    # Import Blueprints INSIDE function
    # -----------------------------------
    from ..routes.auth import auth_bp
    from ..routes.products import product_bp
    from ..routes.cart import cart_bp
    from ..routes.orders import order_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(product_bp, url_prefix="/api")
    app.register_blueprint(cart_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")

    return app
