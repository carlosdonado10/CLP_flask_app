from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField, SelectField, PasswordField
from wtforms.validators import InputRequired, ValidationError, Email, DataRequired


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


class boxesParams(FlaskForm):
    num_types = SelectField('Types of boxes to use', choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                                                              ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)])
    boxX = FloatField("Box Width")
    boxY = FloatField("Box Depth")
    boxZ = FloatField("Box Height")
    num_boxes = IntegerField("Number of Boxes")
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Sign In')