from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error":"Token missing"}), 401

        try:
            decoded = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
        except:
            return jsonify({"error":"Invalid token"}), 401

        return f(decoded, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def wrapper(decoded, *args, **kwargs):
        if decoded["role"] != "admin":
            return jsonify({"error":"Admin only"}), 403
        return f(decoded, *args, **kwargs)
    return wrapper
