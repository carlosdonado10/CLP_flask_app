from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField, SelectField, PasswordField, FieldList, FormField
from wtforms.validators import InputRequired, ValidationError, Email, DataRequired, EqualTo
from application.models import User, Dispatch


def validate_dimensions(form, field):
    if field.data is None:
        raise ValidationError("")
    if not str(field.data).replace('.', '').isnumeric():
        raise ValidationError(f"{field.data} - Please supply numeric values")
    elif field.data < 0:
        raise ValidationError("Please supply positive values")
    elif field.data == 0:
        raise ValidationError("Please supply non-zero values")


class ContainerParams(FlaskForm):
    containerX = FloatField('Container Width', validators=[validate_dimensions])
    containerY = FloatField('Container Depth', validators=[validate_dimensions])
    containerZ = FloatField('Container Height', validators=[validate_dimensions])
    submit = SubmitField()


class SingleBox(FlaskForm):
    boxX = FloatField("Box Width")
    boxY = FloatField("Box Depth")
    boxZ = FloatField("Box Height")
    num_boxes = IntegerField("Number of Boxes")


class boxesParams(FlaskForm):
    boxes = FieldList(FormField(SingleBox), min_entries=2)
    add_box = SubmitField(label='Add Box')
    submit = SubmitField()
    fav_name = StringField(label="Dispatch name") # TODO: Make unique
    favorites = SubmitField(label="Save to Favorites")


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    # TODO: Validate password conditions (has number etc.)
