from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

# Initialize extensions but don't bind to app yet
mongo = PyMongo()
jwt = JWTManager()