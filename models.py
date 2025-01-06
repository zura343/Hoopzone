from ext import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class BaseModel():
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


class Jersey(db.Model, BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    image = db.Column(db.String())
    rating = db.Column(db.Float(), default=0)
    total_ratings = db.Column(db.Integer(), default=0)
    rating_count = db.Column(db.Integer(), default=0)


class Tickets(db.Model, BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    image = db.Column(db.String())
    description = db.Column(db.String)


class Player(db.Model, BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    player = db.Column(db.String())
    team = db.Column(db.String())
    gp = db.Column(db.Integer())
    pts = db.Column(db.Float())
    fgm = db.Column(db.Float())
    fga = db.Column(db.Float())
    fg_pct = db.Column(db.Float())
    three_pm = db.Column(db.Float())
    three_pa = db.Column(db.Float())
    three_pct = db.Column(db.Float())
    ftm = db.Column(db.Float())
    fta = db.Column(db.Float())
    ft_pct = db.Column(db.Float())
    oreb = db.Column(db.Float())
    dreb = db.Column(db.Float())
    reb = db.Column(db.Float())
    ast = db.Column(db.Float())
    stl = db.Column(db.Float())
    blk = db.Column(db.Float())
    tov = db.Column(db.Float())
    eff = db.Column(db.Float())
    min = db.Column(db.Float())


class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    age = db.Column(db.Integer())
    role = db.Column(db.String(), default='user')

    def __init__(self, username, password, age, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.age = age
        self.role = role

    def __repr__(self):
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class News(db.Model, BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    date = db.Column(db.String())
    image = db.Column(db.String())
    news = db.Column(db.String())
    link = db.Column(db.String())


class Championships(db.Model, BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    country = db.Column(db.String())
    official_site = db.Column(db.String)
    logo = db.Column(db.String)


class EasternTeams(db.Model, BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    W = db.Column(db.Integer)
    L = db.Column(db.Integer)
    win_percentage = db.Column(db.Integer)
    GB = db.Column(db.Float)
    CONF = db.Column(db.String)
    DIV = db.Column(db.String)
    HOME = db.Column(db.String)
    ROAD = db.Column(db.String)
    Neutral = db.Column(db.String)
    OT = db.Column(db.String)
    LAST10 = db.Column(db.String)
    STREAK = db.Column(db.String)


class WesternTeams(db.Model, BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    W = db.Column(db.Integer)
    L = db.Column(db.Integer)
    win_percentage = db.Column(db.Integer)
    GB = db.Column(db.Float)
    CONF = db.Column(db.String)
    DIV = db.Column(db.String)
    HOME = db.Column(db.String)
    ROAD = db.Column(db.String)
    Neutral = db.Column(db.String)
    OT = db.Column(db.String)
    LAST10 = db.Column(db.String)
    STREAK = db.Column(db.String)


class Games(db.Model, BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    team_1 = db.Column(db.String)
    team_1_img = db.Column(db.String)
    team_2 = db.Column(db.String)
    team_2_img = db.Column(db.String)
    final_score = db.Column(db.String)
