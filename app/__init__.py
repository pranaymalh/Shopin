from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
app=Flask(__name__)
db=MongoEngine()
app.config.from_object(Config)
db.init_app(app)
from app import routes