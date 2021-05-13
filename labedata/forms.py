from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FileField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

#! TODO add length validation
class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    # remember = BooleanField("Remember Me")
    submit = SubmitField()

class RegisterForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired("Обязательно логин")])
    username = StringField("Name, as to be shown in profile", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField()

class NewDatasetForm(FlaskForm):
    dataset = FileField(label="New dataset", validators=[DataRequired()])
    dataset_format = SelectField(label="Input file format", choices=["csv"], validators=[DataRequired()])
    title = StringField()

    data_field = StringField(label="Data field name") # string
    data_field_type = SelectField(label="Data type", choices=["text"])# text, picture, etc
    label_field = StringField(label="Label field name (if exists)")# string
    label_field_type = SelectField(label="Target label type", choices=["binary"], validators=[DataRequired()])# binary, category, number, word
    user_based_labeling = BooleanField(label="Multiuser labeling (labels will be aggregated)")# boolean,

    allow_modify_data = BooleanField(label="Allow data correction")# boolean
    allow_upsert_data = BooleanField(label="Allow data upsertion")# boolean
    allow_delete_data = BooleanField(label="Allow data removal")# boolea
    submit = SubmitField()