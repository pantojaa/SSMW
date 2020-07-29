from endzone import db, login_mgr
from datetime import datetime
from flask_login import UserMixin


@login_mgr.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # primary_key means it is a unique id for user
    first_name = db.Column(db.String(20), nullable=False)  # nullable=False means that we have to have a first name
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # unique=True means that every email will be unique
    img_file = db.Column(db.String(20), nullable=False, default='default.png')
    banner_file = db.Column(db.String(20), nullable=False, default='soccerball.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    events = db.relationship('Event', backref='author', lazy=True)
    gender = db.Column(db.String(20), nullable=False)
    high_school = db.Column(db.String(20))
    sport = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.String(20), nullable=False)
    birth_month = db.Column(db.String(20), nullable=False)
    birth_year = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    about = db.Column(db.String(300), nullable=False, default=' ')
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)

    # --------------
    def __repr__(self):  # how object is printed to console
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}', '{self.img_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary_key means it is a unique id for user
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_image = db.Column(db.String(20), nullable=False, default='temporary.png')
    post_video = db.Column(db.String(20), nullable=False, default='placeholder.mp4')
    likes = db.Column(db.String(20), default='0')

    def __repr__(self):  # how object is printed to console
        return f"Post('{self.title}', '{self.date_posted}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship('EventPost', backref='post', lazy=True)

    def __repr__(self):  # how object is printed to console
        return f"Event('{self.title}', '{self.date}', '{self.time}', '{self.location}', '{self.content}', '{self.user_id}')"


class EventPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    post_image = db.Column(db.String(20), nullable=False, default='temporary.png')
    post_video = db.Column(db.String(20), nullable=False, default='placeholder.mp4')

