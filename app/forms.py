from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username=StringField("Username", validators= [DataRequired()], render_kw={"placeholder": "username"})
    password= StringField("Password", validators=[DataRequired()], render_kw={"placeholder":"password"})
    remember_me= BooleanField("Remember me")
    submit= SubmitField("Login")


class RegistrationForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired()], render_kw={"placeholder":"username"})
    email= StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder":"email"})
    password=PasswordField("Password", validators=[DataRequired(), EqualTo("password2")], render_kw={"placeholder":"password"})
    password2=PasswordField("Password2", validators=[DataRequired()], render_kw={"placeholder":"password confirmation"})
    submit= SubmitField("Register")

    def validate_username(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Chosen username is not available, please change your username and try again")

    def validate_email(self, email):
        email= User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("This email already exist, please change it and try again")
        