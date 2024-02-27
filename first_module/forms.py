from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, Length

class LoginForm(FlaskForm):
    name = StringField("Имя: ", validators=[DataRequired(), Length(min=4, max=17)])
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти")