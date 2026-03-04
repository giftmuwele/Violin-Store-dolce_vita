import jwt
from functools import wraps
from flask import request, jsonify
import os
import datetime


# ---------------------------------------------------
# GENERATE JWT
# ---------------------------------------------------
def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    return token


# ---------------------------------------------------
# TOKEN REQUIRED DECORATOR
# ---------------------------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            decoded = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(decoded, *args, **kwargs)

    return decorated


# ---------------------------------------------------
# ADMIN REQUIRED
# ---------------------------------------------------
def admin_required(f):
    @wraps(f)
    def decorated(decoded, *args, **kwargs):
        if decoded.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return f(decoded, *args, **kwargs)

    return decorated