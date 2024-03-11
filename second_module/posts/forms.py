from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired

class PostForm(FlaskForm):
    title = StringField("Post Name: ", validators=[Length(min=1, max=10), DataRequired()])
    body = TextAreaField("Post Description: ", validators=[Length(min=1, max=50), DataRequired()])
    submit = SubmitField("Send")