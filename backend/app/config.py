import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SGOCSPX-C6XpcHs4CCoINf3zW8HczZ6WYpUVs")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    GOOGLE_CLIENT_ID = os.getenv("865720164989-ap4dpnm1vialmn0psm314aojmu9p2lms.apps.googleusercontent.com")
