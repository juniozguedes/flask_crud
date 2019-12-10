from app import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
import random
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #if unauthorized, redirects to login
login_manager.login_message = 'You need to login!'

migrate = Migrate(app, db)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    nickname = db.Column(db.String(30))
    tweets = db.relationship('Tweets', backref='user', lazy=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    master = db.Column(db.Boolean, nullable=True, default=False)

class Tweets(db.Model):

    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    tweet_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner_username = db.Column(db.String(30))
    title = db.Column(db.Text)
    slug = db.Column(db.Text)
    content = db.Column(db.Text)
    short = db.Column(db.Text)
    description = db.Column(db.Text)
    entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    uniquekey = db.Column(db.Text, unique=True)
    pageviews =  db.Column(db.Integer, default = 0)

def top_post():
    posts = Tweets.query.all()
    lista = []
    for numero in posts:
        lista.append(numero.pageviews)
    return Tweets.query.filter_by(pageviews=max(lista)).first()

def all_posts():
    return Tweets.query.all()

def recent_post():
    return Tweets.query.order_by(Tweets.id.desc()).first()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):

  if user_id is None:
    folllowers = query.all()
    return followers

  return User.query.get(int(user_id))