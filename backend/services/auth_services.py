from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from flask import current_app
from app.extensions import mysql
import jwt, datetime
import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
    app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")

    return app

def verify_google_token(token):
    try:
        return id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            current_app.config["865720164989-ap4dpnm1vialmn0psm314aojmu9p2lms.apps.googleusercontent.com"] #client Id
        )
    except:
        return None


def find_or_create_user(idinfo):
    email = idinfo["email"]
    name = idinfo["name"]
    google_id = idinfo["sub"]
    picture = idinfo.get("picture")

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if not user:
        cur.execute("""
            INSERT INTO users(name,email,google_id,profile_pic)
            VALUES(%s,%s,%s,%s)
        """, (name,email,google_id,picture))
        mysql.connection.commit()

        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

    return user


def generate_jwt(user):
    return jwt.encode({
        "user_id": user[0],
        "role": user[5],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, current_app.config["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s"], algorithm="HS256")## secret key
