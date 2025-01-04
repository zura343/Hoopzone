from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
from wtforms.fields import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, DateField, SelectField, FloatField
from wtforms.validators import DataRequired, length, Optional, equal_to, ValidationError,NumberRange

from models import User
class EditJerseyForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), length(min=8, max=16)])
    price = IntegerField("Price", validators=[DataRequired()])
    image = FileField("Image", validators=[Optional()])
    submit = SubmitField("Save")


class JerseyForm(FlaskForm):
    name = StringField("player name", validators=[DataRequired(), length(min=8, max=16)])
    price = IntegerField("jersey price", validators=[DataRequired()])
    image = FileField("image", validators=[FileRequired(), FileSize(5000000), FileAllowed(["jpg", "png"])])
    submit = SubmitField("save")


class RegisterForm(FlaskForm):
    username = StringField("username",  validators=[DataRequired()])
    age = DateField("age", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), length(min=8, max=16)])
    repeat_password = PasswordField("repeat password", validators=[equal_to("password")])
    register = SubmitField("register")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("This username is already taken. Please choose another one.")



class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), length(min=8, max=16)])
    login = SubmitField("log in")


class RatingForm(FlaskForm):
    rating = IntegerField('Rate this jersey', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating')


class EditStatsForm(FlaskForm):
    player = StringField("player name", validators=[Optional()])
    team = StringField("player team", validators=[Optional()])
    gp = FloatField("game played", validators=[DataRequired()])
    pts = FloatField("point", validators=[DataRequired()])
    fgm = FloatField("fild goal made", validators=[DataRequired()])
    fga = FloatField("fild goal attempt", validators=[DataRequired()])
    fg_pct = FloatField("fild goal percentage", validators=[DataRequired()])
    three_pm = FloatField("tree pointer made", validators=[DataRequired()])
    three_pa = FloatField("tree pointer attempt", validators=[DataRequired()])
    three_pct = FloatField("tree pointer percentage", validators=[DataRequired()])
    ftm = FloatField("free throw made", validators=[DataRequired()])
    fta = FloatField("free throw attempt", validators=[DataRequired()])
    ft_pct = FloatField("free throw percentage", validators=[DataRequired()])
    oreb = FloatField("offense rebounds", validators=[DataRequired()])
    dreb = FloatField("defense rebounds", validators=[DataRequired()])
    reb = FloatField("rebounds", validators=[DataRequired()])
    ast = FloatField("assist", validators=[DataRequired()])
    stl = FloatField("steal", validators=[DataRequired()])
    blk = FloatField("block", validators=[DataRequired()])
    tov = FloatField("turn over", validators=[DataRequired()])
    eff = FloatField("eff", validators=[DataRequired()])
    min = FloatField("minutes", validators=[DataRequired()])
    submit = SubmitField('save')
