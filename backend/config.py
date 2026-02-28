import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "flask-secret-key"
    JWT_SECRET_KEY = "THIS_IS_A_SUPER_LONG_32_CHAR_JWT_SECRET_KEY_123456"
    JWT_TOKEN_LOCATION = ["headers"]   
    JWT_COOKIE_CSRF_PROTECT = False    

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/resume_builder?charset=utf8mb4"

