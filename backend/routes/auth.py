from flask import Blueprint, request, jsonify
from app.extensions import mysql
from ..utils.decorators import generate_token
from google.oauth2 import id_token
from google.auth.transport import requests
import os

auth_bp = Blueprint("auth", __name__)


# ---------------------------------------------------
# GOOGLE LOGIN
# ---------------------------------------------------
@auth_bp.route("/auth/google", methods=["POST"])
def google_login():
    try:
        data = request.get_json()
        token = data.get("credential")

        if not token:
            return jsonify({"error": "Missing token"}), 400

        # Verify token with Google
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            os.getenv("GOOGLE_CLIENT_ID")
        )

        email = idinfo["email"]
        name = idinfo.get("name")
        google_id = idinfo.get("sub")
        profile_pic = idinfo.get("picture")

        cur = mysql.connection.cursor()

        # Check if user exists
        cur.execute("SELECT id, role FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        if user:
            user_id = user[0]
            role = user[1]
        else:
            # Insert new user
            cur.execute("""
                INSERT INTO users (name, email, google_id, profile_pic)
                VALUES (%s, %s, %s, %s)
            """, (name, email, google_id, profile_pic))
            mysql.connection.commit()

            user_id = cur.lastrowid
            role = "user"

        # Generate JWT
        jwt_token = generate_token(user_id, role)

        return jsonify({
            "token": jwt_token,
            "role": role
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid Google token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500