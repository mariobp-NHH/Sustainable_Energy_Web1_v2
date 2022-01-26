from datetime import datetime
from webse import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    course = db.Column(db.String(60), unique=False, nullable=False)
    moduls = db.relationship('Moduls', backref='author', lazy=True)
    announcements = db.relationship('Announcement', backref='author', lazy=True)
    postsm = db.relationship('Chat', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    chat_module = db.Column(db.String(100), nullable=False)
    chat_group = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Chat('{self.title}', '{self.date_posted}')"

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Announcement('{self.title}', '{self.date_posted}')"

class Moduls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_mo = db.Column(db.String(100), nullable=False)
    title_ch = db.Column(db.String(100), nullable=False)
    question_num = db.Column(db.Integer)
    question_str = db.Column(db.String(100))
    question_result = db.Column(db.Integer)
    question_option = db.Column(db.Integer, nullable=True)
    question_section = db.Column(db.String(100), nullable=True)
    date_exercise = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Moduls('{self.question_str}', '{self.question_result}', '{self.date_exercise}')"

