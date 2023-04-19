from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

database = SQLAlchemy()
bcrypt = Bcrypt()

def connect_database(app):
    """ Connect to database """
    database.app = app
    database.init_app(app)



class User(database.Model):
    """ User model """
    __tablename__ = 'users'


    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register an account """
        return cls(username=username, password=(bcrypt.generate_password_hash(password)).decode('utf8'), email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """ Check if user exists and informations are correct """
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        
    @classmethod
    def get_user(cls, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return False

    username  = database.Column(database.String(20), nullable=False, primary_key=True, unique=True)

    password  = database.Column(database.Text, nullable=False)

    email = database.Column(database.String(50), nullable=False, unique=True)

    first_name = database.Column(database.String(30), nullable=False)

    last_name = database.Column(database.String(30), nullable=False)


class Feedback(database.Model):
    """ Feedback model """
    __tablename__ = 'feedbacks'

    id = database.Column(database.Integer, nullable=False, primary_key=True, autoincrement=True)

    title  = database.Column(database.String(100), nullable=False)

    content  = database.Column(database.Text, nullable=False)

    username = database.Column(database.String(20), database.ForeignKey('users.username'), nullable=False)

    user = database.relationship('User', backref='feedbacks')
