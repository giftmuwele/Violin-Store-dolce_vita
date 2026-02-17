from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import mysql, bcrypt
from routes.orders import order_bp
register_blueprint(order_bp, url_prefix="/api")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    mysql.init_app(app)
    bcrypt.init_app(app)

    from ..routes.auth import auth_bp
    from ..routes.products import product_bp
    from ..routes.cart import cart_bp
    from ..routes.orders import order_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(product_bp, url_prefix="/api")
    app.register_blueprint(cart_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")

    return app
