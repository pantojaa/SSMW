from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# creates an instance of flask framework
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'a30a3c896a6bdbc652292a2b4b7af9e1'

# SQLAlchemy instance for database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_mgr = LoginManager(app)
login_mgr.login_view = 'login'  # function name of our route
login_mgr.login_message_category = 'info'

# Placed here to avoid circular imports
from endzone import routes

