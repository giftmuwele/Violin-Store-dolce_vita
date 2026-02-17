from flask import Blueprint, request, jsonify
from ..services.auth_services import verify_google_token, find_or_create_user, generate_jwt

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    token = request.json.get("token")

    idinfo = verify_google_token(token)
    if not idinfo:
        return jsonify({"error":"Invalid Google token"}), 401

    user = find_or_create_user(idinfo)
    jwt_token = generate_jwt(user)

    return jsonify({
        "token": jwt_token,
        "role": user[5],
        "name": user[1]
    })
