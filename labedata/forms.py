from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FileField, SelectField
from wtforms.validators import DataRequired, Email



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    # password = StringField("Password", validators=[DataRequired()])
    # remember = BooleanField("Remember Me")
    submit = SubmitField()

class DataSetUploadForm(FlaskForm):
    dataset = FileField(label="New dataset")
    format_ = SelectField(label="Format", choices=["csv"])
    
    submit = SubmitField()