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
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # new stuff added
    high_school = db.Column(db.String(20))
    sport = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(20), nullable=False)
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

    def __repr__(self):  # how object is printed to console
        return f"Post('{self.title}', '{self.date_posted}')"
