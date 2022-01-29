from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from webse.announcements.routes import announcements
from webse.app_calculator.routes import app_calculator
from webse.app_module.routes import app_module
from webse.chats.routes import chats
from webse.home.routes import home
from webse.se_module.routes import se_module
from webse.statistics.routes import statistics
from webse.users.routes import users

app.register_blueprint(announcements)
app.register_blueprint(app_calculator)
app.register_blueprint(app_module)
app.register_blueprint(chats)
app.register_blueprint(home)
app.register_blueprint(se_module)
app.register_blueprint(statistics)
app.register_blueprint(users)